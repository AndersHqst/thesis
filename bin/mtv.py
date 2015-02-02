from settings import *
import itemsets
from model import Model
from heurestic import h
from utils.timer import *
from graph import Graph

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

        # Main model where everythin is added to.
        # We use this to compute the overall run results
        self.main_model = Model(self)
        self.main_model.iterative_scaling()
        self.main_model.C = initial_C

        self.models = []

        # Cache for merged models
        self.model_cache = {}

        # Cached queries
        self.query_cache = {}


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


    def run(self):
        """
        Run the mtv algorithm
        """

        self.main_model.BIC_scrores['initial_score'] = self.main_model.score()
        self.build_independent_models()

        # Add itemsets until we have k
        # We ignore an increasing BIC score, and always mine k itemsets
        while len(self.main_model.C) < self.k:

            X = self.find_best_itemset()

            if not (self.validate_best_itemset(X)):
                break

            self.main_model.add_to_summary(X)
            self.build_independent_models()


    def build_independent_models(self):
        # Clear old models
        self.models = []

        # If C is empty, we just need one empty model
        if len(self.main_model.C) == 0:
            model = Model(self)
            model.iterative_scaling()
            self.models.append(model)

        # Create all disjoint models
        else:
            graph = Graph()
            for itemset in self.main_model.C:
                graph.add_node(itemset)
            for disjoint_C in graph.disjoint_itemsets():
                model = Model(self)
                model.C = disjoint_C
                model.union_of_C = itemsets.union_of_itemsets(disjoint_C)
                model.iterative_scaling()
                self.models.append(model)

        print 'Independent models: ', len(self.models)


    def query(self, y):
        """
        Query using necessary models w.r.t y
        """

        intersected_models = []
        for model in self.models:
            if y & model.union_of_C != 0:
                intersected_models.append(model)

        # No intersection. Use any model
        if len(intersected_models) == 0:
            return self.models[0].query(y)

        # 1 intersecting model, use that
        if len(intersected_models) == 1:
            return intersected_models[0].query(y)

        # More than 1 model intersected
        # Get itemsets in the Cs
        coverage = []
        for intersected_model in intersected_models:
            coverage += intersected_model.C

        # Check cache
        coverage.sort()
        key = tuple(coverage)
        if key in self.model_cache:
            return self.model_cache[key].query(y)

        # Create new intersecting model, and cache it
        merged_model = Model(self)
        merged_model.C = coverage
        merged_model.union_of_C = itemsets.union_of_itemsets(merged_model.C)
        merged_model.iterative_scaling()
        self.model_cache[key] = merged_model

        return merged_model.query(y)


    def cached_itemset_query(self, X):
        """
        Helper function to cache queries.
        Note this can only be used from e.g. FindBestItemSet
        when the model parameters are not altered between cache hits.
        :param X: Queried itemset
        :return: Query result
        """

        estimate = 0.0

        if X == 6:
            pass

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