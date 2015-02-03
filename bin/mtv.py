from settings import *
import itemsets
from model import Model
from heurestic import h
from utils.timer import *
from graph import Graph
from utils.timer import *
from utils.counter import *
from math import log

class MTV(object):

    def __init__(self, D, initial_C=[], k=DEFAULT_K, m=DEFAULT_M, s=DEFAULT_S, z=DEFAULT_Z):
        super(MTV, self).__init__()

        # Mine up to k itemsets
        self.k = k

        # Maximum itemset size
        self.m = m

        # Support
        self.s = s

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
        self.union_of_C = 0

        self.BIC_scores = {}
        self.heuristics = {}

        self.models = []

        # Cache for merged models
        self.model_cache = {}

        # Cached queries
        self.query_cache = {}


    def run(self):
        """
        Run the mtv algorithm
        """

        self.build_independent_models()
        self.BIC_scores['initial_score'] = self.models[0].score()

        # Run until we have converged
        while not self.finished():

            X = self.find_best_itemset()

            if not (self.validate_best_itemset(X)):
                break

            self.add_itemset(X)


    def query(self, y):
        """
        Query using necessary models w.r.t y
        """

        # No intersection. Use models[0]
        # which holds disjoint singletons
        if y & self.union_of_C == 0:
            return self.models[0].query(y)


        # query intersected models independently
        mask = y
        p = 1.0


        for model in self.models:

            # Is this an intersected model?
            if y & model.union_of_C != 0:

                # get intersection
                intersection = model.union_of_C & mask

                # remove from mask
                mask = intersection ^ mask

                # query the intersected model
                p *= model.query(intersection)

        # disjoint singletons
        p *= self.models[0].query(mask)

        return p


    def score(self):

        total_score = 0

        for model in self.models:
            total_score += model.score()

        total_score += 0.5 * len(self.C) * log(len(self.D), 2)

        return total_score


    def finished(self):
        """
        Return True if the model has converged, or if k is provided, that k itemsets have been found.
        :return:
        """
        if not (self.k is None):
            return self.k < len(self.C)

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

        self.build_independent_models()
        # Compute score
        self.BIC_scores[X] = self.score()


    def build_independent_models(self):
        """
        Builds model for each disjoint set of C
        :return:
        """
        timer_start('Build independent models')

        # Clear old models
        self.models = []

        # Hack to only use one model
        # if True:
        #     model = Model(self)
        #     model.C = self.C
        #     model.I = self.I
        #     model.union_of_C = itemsets.union_of_itemsets(self.C)
        #     model.iterative_scaling()
        #     self.models.append(model)
        #     return


        # If C is empty, we just need one empty model
        if len(self.C) == 0:
            model = Model(self)
            model.I = model.I.union(self.I)
            model.iterative_scaling()
            self.models.append(model)

        # Create all disjoint models
        else:
            graph = Graph()
            for itemset in self.C:
                graph.add_node(itemset)

            I_copy = self.I.copy()
            for disjoint_C in graph.disjoint_itemsets():
                model = Model(self)
                model.C = disjoint_C
                model.I = itemsets.singletons(model.C)
                I_copy = I_copy - model.I
                model.union_of_C = itemsets.union_of_itemsets(disjoint_C)
                model.iterative_scaling()
                self.models.append(model)
            self.models[0].I = self.models[0].I.union(I_copy)
            self.models[0].iterative_scaling()

        timer_start('Build independent models')
        counter_max('Independent models', len(self.models))

    def cached_itemset_query(self, X):
        """
        Helper function to cache queries.
        Note this can only be used from e.g. FindBestItemSet
        when the model parameters are not altered between cache hits.
        :param X: Queried itemset
        :return: Query result
        """

        estimate = 0.0

        if X in self.query_cache:
            estimate = self.query_cache[X]
        else:
            estimate = self.query(X)
            self.query_cache[X] = estimate

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
        Z = self.find_best_itemset_rec(0, self.I.copy(), [(0,0)])
        timer_stop('Find best itemset')

        # Edge case, where we only find singletons not exactly described by the model
        # We search the top 10 Zs to see if there was a non singleton itemset
        for z in Z:
            if not (z in self.I) and z != 0:
                return z[0]
        print 'No valid z in Z: ', Z
        return Z[0][0]


    def find_best_itemset_rec(self, X, Y, Z, X_length=0, singleton_restrictions=None):
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