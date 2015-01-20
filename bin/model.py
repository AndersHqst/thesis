from __future__ import division
from charitems import to_binary, to_chars
from math import log
from itertools import combinations, permutations
from memoisation import memoise
from block import Block
from timer import *
from counter import *
from settings import *
import itemsets
from heurestic import h
import sys
sys.setrecursionlimit(1500)

class Model(object):

    def __init__(self, D, k=DEFAULT_K, m=DEFAULT_M, s=DEFAULT_S, z=DEFAULT_Z):
        super(Model, self).__init__()

        # Model parameters
        self.u0 = 0
        self.U = {}

        # summary
        self.C = list()

        # Mine up to k itemsets
        self.k = k

        # Maximum itemset size
        self.m = m

        # Support
        self.s = s

        # Number of candidate itemsets FindBestItemSet should search for
        # Will result in a list of top-z highest heuristics
        self.z = z

        # Heurestics from h() for X in C at the time X was added
        self.heurestics = {}

        # BIC scores for X in C at the time X was added
        self.BIC_scrores = {}

        # Block w.r.t C
        self.T_c = []

        # Dataset
        self.D = D

        # Singletons
        self.I = set()

        # Cached queries in FindBestItemSet
        self.query_cache = {}

        # Cached frequency counts in D
        self.fr_cache = {}


    def p(self, T, y):
        """
        Return a model estiamte for y in block T
        :param T: A block
        :param y: Itemset
        :return: Model estimate for y in T
        """
        res = 1.0

        for x in self.C:
            assert not (x in self.I), "Singletons are not in summary calling p()"
            if itemsets.contains(T.union_of_itemsets, x):
                res = res * self.U[x]

        return self.u0 * res * T.block_weight


    def old_model(self, t):
        res = 1.0

        for x in self.C:
            if itemsets.contains(t, x):
                res = res * self.U[x]

        return self.u0 * res


    def closure(self, y):
        """
        Returns a closure of itemset in C that har subsets of y
        :param y: Itemset to create clojure for
        :return: Clojure over C w.r.t y
        """
        closure = set()

        for itemset in self.C:
            if itemset & y == itemset:
                closure.add(itemset)

        return closure


    def independence_estimate(self, y):
        independence_estimate = 1.0
        for i in itemsets.singletons_of_itemset(y):
            independence_estimate *= self.U[i] / (1 + self.U[i])

        counter_inc('Independence estimates')

        return independence_estimate


    def query(self, y):
        """
        Query the probability on an itemset y.
        :param y: Itemset
        :return: Estimate of y
        """

        counter_inc('Total queries')

        if y & self.T_c[0].union_of_itemsets == 0:
            return self.independence_estimate(y)

        counter_inc('Block queries')

        cls = self.closure(y)
        T_c = self.compute_block_weights(y, cls)

        timer_start('Compute p')
        estimate = 0.0
        for T in T_c:
            estimate += self.p(T, y)
        timer_stop('Compute p')

        return estimate


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


    def cached_itemset_stats(self, X):
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

        # reset query cache
        self.query_cache = {}

        timer_start('Find best itemset')
        Z = self.find_best_itemset_rec(0, self.I.copy(), [(0,0)])
        timer_stop('Find best itemset')

        # Edge case, where we only find singletons not exactly described by the model
        # We search the top 10 Zs to see if there was a non singleton itemset
        for z in Z:
            if not (z in self.I) and z != 0:
                return z
        print 'No valid z in Z: ', Z
        return Z[0]

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

        p_X = self.cached_itemset_stats(X)
        fr_Z = self.fr(Z[-1][0])
        p_Z = self.cached_itemset_stats(Z[-1][0])

        h_X = h(fr_X, p_X)
        if h_X > Z[-1][1] or len(Z) < self.z:
            Z.append((X, h_X))
            # Sort by descending  heuristic
            Z.sort(lambda x, y: x[1] < y[1] and 1 or -1)
            if self.z < len(Z):
                Z.pop()

        XY = X | itemsets.union_of_itemsets(Y)
        fr_XY = self.fr(XY)
        p_XY = self.cached_itemset_stats(XY)

        b = max(h(fr_X, p_XY), h(fr_XY, p_X))

        if Z[0][0] == 0 or b > Z[-1][1]:
            if self.m == 0 or X_length < self.m:
                while 0 < len(Y):
                    y = Y.pop()
                    Z = self.find_best_itemset_rec(X | y, Y.copy(), Z, X_length + 1)

        return Z

    def find_best_itemset_iter(self, X, I, Z, model, s, m, X_length=0):
        """
        :param X: itemset
        :param Y: remaining itemsets
        :param Z: currently best itemset
        :param s: min support
        :param m: max itemset size
        :param X_length: number of items in X. No pretty, but since X is an int,
                         this is the fastest way to know its length
        :return: Best itemset Z
        """

        stack = []
        stack.append((X, itemsets.union_of_itemsets(I), X_length))
        d = set()
        while 0 < len(stack):
            X, Y, X_length = stack.pop()

            if not (X, Y) in d:

                d.add((X, Y))

                if m is None or X_length < m:

                    # Initially all I
                    Ys_copy = Y

                    # If not bounded, add all Xy to the stach
                    for y in I:

                        if X & y == 0 and Ys_copy & y == y:
                            Xy = X | y
                            fr_X = self.fr(Xy)
                            if fr_X < s:
                                continue
                            Ys_copy = Ys_copy ^ y

                            p_Xy = self.cached_itemset_stats(Xy)

                            fr_Z = self.fr(Z[0][0])
                            p_Z = self.cached_itemset_stats(Z[0][0])

                            h_X = h(fr_X, p_Xy)
                            h_Z = h(fr_Z, p_Z)
                            if h_X > h_Z or len(Z) < 10:
                                Z.append((Xy, h_X))
                                # Sort by descending  heuristic
                                Z.sort(lambda x, y: x[1] < y[1] and 1 or -1)
                                if 10 < len(Z):
                                    Z.pop()

                            XY = Xy | Ys_copy
                            fr_XY = self.fr(XY)

                            p_XY = self.cached_itemset_stats(XY)

                            b = max(h(fr_X, p_XY), h(fr_XY, p_Xy))

                            if Z[0][0] == 0 or b > h_Z:
                                stack.append((Xy, Ys_copy, X_length + 1))

        return Z

    def compute_blocks(self, set_prob=False):
        """
            Compute the set of blocks that C infer
            return: Topologically sorted blocks T_c
        """

        timer_start('Compute blocks')

        T_c = list()
        T_unions = set()

        # iterate the combination sizes in reverse
        a = range(len(self.C)+1)[::-1]
        for i in a:
            choose = i
            for comb in combinations(self.C, choose):
                union = itemsets.union_of_itemsets(comb)

                if not union in T_unions:
                    T_unions.add(union)
                    T = Block()
                    T.union_of_itemsets = union
                    if set_prob:
                        self.C_masks[union] = comb
                        self.cached_queries[union] = self.query(union)
                    T.singletons = itemsets.singletons_of_itemsets(comb)
                    T.itemsets = set(comb)
                    T_c.append(T)

        timer_stop('Compute blocks')
        return T_c


    def compute_block_sizes(self, T_c):
        for T in T_c:
            T.cummulative_block_size = 2 ** (len(self.I) - len(to_chars(T.union_of_itemsets)))
        for i, Ti in enumerate(T_c):
            Ti.block_size = Ti.cummulative_block_size
            for Tj in T_c[:i]:
                if Ti < Tj:
                    Ti.block_size = Ti.block_size - Tj.block_size
        return T_c

    def block_in_closure(self, T, closure):
        for c in closure:
            if not (c in T.itemsets):
                return False
        return True

    def compute_block_weights(self, y, closure):

        U = self.U
        blocks = []

        total_weight = 1
        for i in self.I:
            total_weight *= (1 + U[i])

        timer_start('Cummulative weight')
        for T in self.T_c:

            if self.block_in_closure(T, closure):

                blocks.append(T)

                T.cummulative_block_weight = total_weight

                # Remove singletons from y already covered by the block
                mask = y & T.union_of_itemsets
                ys = mask ^ y
                for i in itemsets.singletons_of_itemset(ys):
                    T.cummulative_block_weight *= U[i] * (1 / (1 + U[i]))

                for i in T.singletons:
                    T.cummulative_block_weight *= U[i] * (1 / (1 + U[i]))


        timer_stop('Cummulative weight')

        timer_start('Block weight')
        for i, Ti in enumerate(blocks):
            Ti.block_weight = Ti.cummulative_block_weight
            for Tj in blocks[:i]:
                if Ti < Tj:
                    Ti.block_weight = Ti.block_weight - Tj.block_weight

        return blocks

    def iterative_scaling(self):

        # Initialize U and u0
        self.u0 = 2 ** -len(self.I)
        _C = self.I.union(self.C)
        for c in _C:
            self.U[c] = 1.0

        timer_start('Iterative scaling')

        iterations = 0
        epsilon = 1e-5

        while iterations < 100:

            max_error = 0

            for x in _C:

                estimate = self.query(x)

                if self.fr(x) == 0 or estimate == 0:
                    assert False, 'itemset %d has frequency=%f and p=%f. It should not be added to the summary' % (x, self.fr(x), estimate)
                    exit()

                fr_x = self.fr(x)
                if  abs(1 - fr_x) < float_precision:
                    print 'fr_x was 1'
                    fr_x = 0.9999999999
                if  abs(1 - estimate) < float_precision:
                    print 'estimate was 1'
                    p = 0.9999999999


                self.U[x] = self.U[x] * (fr_x / estimate) * ((1 - estimate) / (1 - fr_x))

                self.u0 = self.u0 * (1 - fr_x) / (1 - estimate)

                max_error = max(max_error, 1 - min(fr_x, estimate) / max(fr_x, estimate))

                counter_max('Iterative scaling max iterations', iterations)

            iterations += 1

            if max_error < epsilon:
                break

        timer_stop('Iterative scaling')


    def mtv(self):
        """ """
        global model

        # TODO move this data cleaning elsewhere
        tmp = []
        for i in self.D:
            if i != 0:
                tmp.append(i)
        self.D = tmp

        self.I = itemsets.singletons(self.D)

        self.T_c = self.compute_blocks()

        # Initialize the model
        self.iterative_scaling()

        # Save initial BIC score for the independence distribution
        self.BIC_scrores['initial_score'] = self.score()

        # Add itemsets until we have k
        while len(self.C) < self.k:

            X, heurestic = self.find_best_itemset()
            assert not (X in self.I), 'X was a singleton! These should not be possible from the heurestic'

            if X == 0:
                print 'Best itemset found was the empty set (0). This probably ' \
                      'means the heurestic could not find any itemset ' \
                      'not already predicted by the model. Exiting MTV'
                break

            # Add X to summary
            self.C.append(X)
            self.heurestics[X] = heurestic

            self.T_c = self.compute_blocks()

            # Update model
            self.iterative_scaling()

            # Compute score
            cur_score = self.score()
            self.BIC_scrores[X] = cur_score


    def score(self):
        try:
            _C = self.I.union(self.C)
            U = self.U
            u0 = self.u0
            D = self.D

            return -1 * ((len(D)) * (log(u0, 2) + sum([self.fr(x) * log(U[x], 2) for x in _C]))) + 0.5 * len(_C) * log(len(D))

        except Exception, e:
            print 'Exception in score function'
            print 'Summary: ', _C
            b = 'YES'
            if u0 < 0:
                b = 'NO'
            print 'u0 %f above 0: %s' % (u0, b)
            print 'U: ', U
            exit()

    def is_in_sumamry(self, y):
        """
        :param y: Itemset to look for
        :param C: Summary
        :return: Ture if y is in C
        """
        for x in self.C:
            if y == x:
                return True
        return False

    def total_probability(self):
        """ Assert and print the total probability of the model """
        total_prob = 0.0
        for T in self.T_c:
            total_prob += self.p(T, 0)
        assert abs(total_prob - 1.0) < 0.0001, "Total probability was: %f " % total_prob
        print 'total prob: ', total_prob

