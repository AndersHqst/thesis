from settings import *
import itemsets
from model import Model
from heurestic import h
from utils.timer import *
from graph import Graph
from utils.timer import *
from utils.counter import *
from math import log
from time import time

class MTV(object):

    def __init__(self, D, initial_C=[], k=DEFAULT_K, m=DEFAULT_M, s=DEFAULT_S, z=DEFAULT_Z, v=DEFAULT_V, headers=None):
        super(MTV, self).__init__()

        # Mine up to k itemsets
        self.k = k

        # Maximum itemset size
        self.m = m

        # Support
        self.s = s

        self.v = v

        self.headers = headers

        # Number of candidate itemsets FindBestItemSet should search for
        # Will result in a list of top-z highest heuristics
        self.z = z

        # Dataset, is it right to always remove empty rows?
        tmp = []
        for i in D:
            if i != 0:
                tmp.append(i)
        self.D = tmp

        # Singletons
        self.I = itemsets.singletons(self.D)

        # Cached frequency counts in D
        self.fr_cache = {}

        # Global summary
        self.C = initial_C
        self.union_of_C = itemsets.union_of_itemsets(self.C)

        self.BIC_scores = {}
        self.heuristics = {}

        # Create a model for holding all singletons
        # Singletons not used by model in the graph
        # will be in this model
        self.singleton_model = Model(self)
        self.singleton_model.I = self.I.copy()

        # Graph of independent models
        self.graph = Graph()
        self.__init_graph()

        # Cache for merged models
        self.model_cache = {}

        # Cached queries
        self.query_cache = {}

        # List to track history of disjoint components
        self.independent_components = []

        # List to track history of C size
        self.largest_summary = []

        # List to track history of timings of a loop in mtv
        self.loop_times = []


    def run(self):
        """
        Run the mtv algorithm
        """

        timer_stopwatch('run')

        self.BIC_scores['initial_score'] = self.score()

        # Run until we have converged
        while not self.finished():

            start = time()

            X = self.find_best_itemset()

            if not (self.validate_best_itemset(X)):
                break

            self.add_itemset(X)

            self.loop_times.append(time()-start)

            if self.v:
                print 'Found itemset (%.2f secs): %s, score: %f, models: %d, max(|C|): %d' % (timer_stopwatch_time('run'), itemsets.to_index_list(X, self.headers), self.BIC_scores[X], self.independent_components[-1], self.largest_summary[-1])


    def query(self, y):
        """
        Query using models intersected by y
        """

        timer_start('mtv_query')
        # query intersected models independently
        mask = y
        p = 1.0
        for model in self.graph.independent_models():

            # Is this an intersected model?
            if y & model.union_of_C != 0:

                # get intersection
                intersection = model.union_of_C & mask

                # remove from mask
                mask = intersection ^ mask

                # query the intersected model
                p *= model.query(intersection)

        # disjoint singletons
        p *= self.singleton_model.query(mask)

        timer_stop('mtv_query')

        return p


    def query_headers(self, itemset_headers):
        """
        Query an itemset by its header names.
        This method will give a ValueError if the
        queried headers are not in the headers property
        of MTV
        :param itemset_headers: A list of headers
        :return: model query of the queried itemset
        """

        # itemset for the provided header names, will throw ValueError
        # if a header name is not in the self.headers property
        itemset = itemsets.itemset_for_headers(self.headers, itemset_headers)

        return self.query(itemset)


    def score(self):

        total_score = self.singleton_model.score()

        for model in self.graph.independent_models():
            total_score += model.score()

        total_score += 0.5 * len(self.C) * log(len(self.D), 2)

        return total_score


    def finished(self):
        """
        Return True if the model has converged, or if k is provided, that k itemsets have been found.
        :return:
        """
        if not (self.k is None):
            return self.k <= len(self.C)

        if 1 < len(self.C):
            # If previous score is lower, the model score has increased
            # and we should finish.
            return self.BIC_scores[self.C[-2]] < self.BIC_scores[self.C[-1]]

        return False


    def add_itemset(self, X):
        """
        Add an itemset X to C and update MTV.
        warning: Adding itemsets to C should always be
         done with this methods, or MTV will be left in an
         invalid state.
        :param X: Itemset to be added to C
        :return:
        """
        heuristic = h(self.fr(X), self.query(X))

        # Add X to global summary
        self.C.append(X)
        self.union_of_C = itemsets.union_of_itemsets(self.C)
        self.heuristics[X] = heuristic

        self.update_graph(X)
        # Compute score
        self.BIC_scores[X] = self.score()


    def __init_graph(self):
        """
        Init the graph with itemsets in C
        :return:
        """

        # Build graph
        for X in self.C:
            self.graph.add_node(X, Model(self))

        # initialize independent models
        # and removed singletons from singleton model
        for model in self.graph.independent_models():
            model.iterative_scaling()
            self.singleton_model.I -= model.I

        # finally initialize the singleton model
        self.singleton_model.iterative_scaling()


    def update_graph(self, X):
        """
        Updates the graph with a new itemset X. This will always results in a new
        model being initialized. The new model's C corresponds to a new graph
        component, that may contain a merge of one or more existing
        graph components.
        """
        timer_start('Build independent models')

        new_model, components = self.graph.add_node(X, Model(self))
        new_model.iterative_scaling()

        # Update the singleton model
        self.singleton_model.I -= new_model.I
        self.singleton_model.iterative_scaling()

        # stats
        self.independent_components.append(len(components))
        largest_C = 0
        for component in components:
            largest_C = max(largest_C, len(component.model.C))
        self.largest_summary.append(largest_C)

        timer_start('Build independent models')
        counter_max('Independent models', len(components))


    def cached_itemset_query(self, X):
        """
        Helper function to cache queries.
        Note this can only be used from e.g. FindBestItemSet
        when the model parameters are not altered between cache hits.
        :param X: Queried itemset
        :return: Query result
        """
        timer_start('Cached query')
        estimate = 0.0

        if X in self.query_cache:
            estimate = self.query_cache[X]
        else:
            estimate = self.query(X)
            self.query_cache[X] = estimate

        timer_stop('Cached query')
        return estimate


    def find_best_itemset(self):
        """
        Find best itemset in the sample
        space defined by I.
        Subject to model parameters z, m, s and
        the heuristic function h
        :return:
        """

        # reset query caches
        self.query_cache = {}
        self.model_cache = {}

        timer_start('Find best itemset')
        Z = self.find_best_itemset_iter(0, self.I.copy(), [(0,0)])
        timer_stop('Find best itemset')

        # Edge case, where we only find singletons not exactly described by the model
        # We search the top 10 Zs to see if there was a non singleton itemset
        for z in Z:
            if not (z in self.I) and z != 0:
                return z[0]
        print 'No valid z in Z: ', Z
        return Z[0][0]


    def find_best_itemset_rec(self, X, Y, Z, X_length=0):
        """
        :param X: itemset
        :param Y: remaining itemsets
        :param Z: currently best itemset
        :param s: min support
        :param m: max itemset size
        :param X_length: number of items in X. No pretty, but since X is an int,
                         this is the fastest way to know its length
        :return: Best itemsets Z
        """

        fr_X = self.fr(X)
        if fr_X < self.s:
            return Z

        p_X = self.cached_itemset_query(X)

        h_X = h(fr_X, p_X)
        if h_X > Z[-1][1] or len(Z) < self.z:
            Z.append((X, h_X))

            # Sort by descending  heuristic
            Z.sort(lambda x, y: x[1] < y[1] and 1 or -1)
            if self.z < len(Z):
                Z.pop()


        XY = X | itemsets.union_of_itemsets(Y)
        fr_XY = self.fr(XY)
        p_XY = self.cached_itemset_query(XY)

        b = max(h(fr_X, p_XY), h(fr_XY, p_X))

        if Z[0][0] == 0 or b > Z[-1][1]:

            if self.m == 0 or X_length < self.m:
                while 0 < len(Y):
                    y = Y.pop()
                    Z = self.find_best_itemset_rec(X | y, Y.copy(), Z, X_length + 1)

        return Z


    def fr(self, x):
        """
        :param x: Itemset
        :return: Frequency of x in D
        """

        if x in self.fr_cache:
            return self.fr_cache[x]

        p = 0.0
        for xi in self.D:
            if itemsets.contains(xi, x):
                p += 1
        p = p / len(self.D)

        assert p <= 1.0

        self.fr_cache[x] = p

        return p


    def validate_best_itemset(self, itemset):
        """
        Returns true if an itemset is valid to be added to C, or false.
        Singletons or the empty set should not be added to C, but this can happen
        in cases where e.g. thresholds for support or min itemset size
        are too strict
        """
        if itemset in self.I:
            print 'X was a singleton! These should not be possible from the heurestic'
            return False

        if itemset == 0:
            print 'Best itemset found was the empty set (0). This could ' \
                      'mean the heurestic could not find any itemset ' \
                      'not already predicted by the model, or above ' \
                      'the provided thresholds. Exiting MTV'
            return False

        return True