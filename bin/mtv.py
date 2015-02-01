#!/usr/bin/env pypy

class MTV(object):

    def __init__(self, D, k=DEFAULT_K, m=DEFAULT_M, s=DEFAULT_S, z=DEFAULT_Z):
        super(MTV, self).__init__()

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

        # Dataset, is it right to always remove empty rows?
        tmp = []
        for i in D:
            if i != 0:
                tmp.append(i)
        self.D = tmp

        # Singletons
        self.I = itemsets.singletons(self.D)

        self.singletons_restricted = None

        # Cached queries in FindBestItemSet
        self.query_cache = {}

        # Cached frequency counts in D
        self.fr_cache = {}

        self.iterative_scaling()




if __name__ == "__main__":
    import main
    import sys
    main.main(sys.argv[1:])