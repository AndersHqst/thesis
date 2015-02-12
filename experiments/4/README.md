Experiment with only bacteria at the lowest levels. These are at level 6. Do not include leafs at lower depths.


Setup:
    Sample abundance counts are made relative to the sample.
    Data is discretized with the maxent discretization.

Questions:

    What is the summary?
        Assert nothing is in same lineage.
        Do we get any of the Faust results?
            Find leaf to leaf in Faust results.
            Is there a connected component in the Faust results graph
            corresponding to the hyper-node we have found.
        Can we query the Faust (leaf) results?
        Does this make sense biologically?
            - Talk to bio about this, show them patterns.
        Build hyper-graph to visualize this.
            Do the patterns overlap?

Report:
    Write about results based on above questions.

Cleaning:
Attributes:  166
discrete dataset cleaning, removed bacteria:  87
Attributes after cleaning:  79

./main.py -f ../experiments/4/Stool_maxent_discretized_nodes_depth_6_005.dat -s 0.1 --debug -v -o ../experiments/4/ -k 10 -H ../experiments/4/Stool_maxent_discretized_nodes_depth_6_005.headers --co-exclusion
/Users/ahkj/pypy-2.4.0-osx64/site-packages/numpy/linalg/_umath_linalg.py:1322: UserWarning: no cffi linalg functions and no _umath_linalg_capi module, expect problems.
  warn('no cffi linalg functions and no _umath_linalg_capi module, expect problems.')



Found itemset (144.11 secs): [16, 17, 19, 20, 25, 26, 47, 91, 184], score: 53243.604494, models: 1, Ci: [1], searched-nodes: 23177758
Found itemset (39.07 secs): [9, 10, 11, 12, 14, 24, 28, 42], score: 53084.431776, models: 2, Ci: [1, 1], searched-nodes: 23178058
Found itemset (29.89 secs): [16, 19, 74, 75, 78, 84, 85, 184], score: 52938.986088, models: 2, Ci: [1, 2], searched-nodes: 23178071
Found itemset (26.30 secs): [80, 81, 89, 91, 184], score: 52807.403626, models: 2, Ci: [1, 3], searched-nodes: 23178069
Found itemset (27.57 secs): [6, 36, 44, 45], score: 52713.775850, models: 3, Ci: [3, 1, 1], searched-nodes: 23178063
Found itemset (28.59 secs): [14, 19, 21, 23, 26, 184], score: 52623.793610, models: 2, Ci: [1, 5], searched-nodes: 23178014
Found itemset (55.45 secs): [8, 10, 17, 24, 50, 184], score: 52543.282367, models: 2, Ci: [1, 6], searched-nodes: 23178018
Found itemset (99.24 secs): [29, 57, 58, 171], score: 52463.650621, models: 3, Ci: [6, 1, 1], searched-nodes: 23178070
Found itemset (29.28 secs): [74, 78, 81, 82, 152], score: 52392.307969, models: 3, Ci: [1, 1, 7], searched-nodes: 23178019
Found itemset (266.13 secs): [3, 4, 10, 12, 14, 20, 184], score: 52327.938809, models: 3, Ci: [1, 1, 8], searched-nodes: 23178007
202 items in 354 transactions

Model predictions:
query [16, 17, 19, 20, 25, 26, 47, 91, 184] with fr 0.104520 query 0.104522
query [9, 10, 11, 12, 14, 24, 28, 42] with fr 0.110169 query 0.110171
query [16, 19, 74, 75, 78, 84, 85, 184] with fr 0.112994 query 0.112999
query [80, 81, 89, 91, 184] with fr 0.135593 query 0.135596
query [6, 36, 44, 45] with fr 0.112994 query 0.112994
query [14, 19, 21, 23, 26, 184] with fr 0.115819 query 0.115819
query [8, 10, 17, 24, 50, 184] with fr 0.107345 query 0.107347
query [29, 57, 58, 171] with fr 0.132768 query 0.132768
query [74, 78, 81, 82, 152] with fr 0.107345 query 0.107349
query [3, 4, 10, 12, 14, 20, 184] with fr 0.104520 query 0.104523

k=10, m=0, s=0.100000

MTV run time:  745.789314032

Summary: 
Heuristic    BIC score   p       |c|     models  Time    Relationship    Itemsets
x.xxxxxx     53429.726044    (No query)      0   0   0   +/-         I+seed
0.460042     53243.604494    0.104522    1   1   144.11      -       [16, 17, 19, 20, 25, 26, 47, 91] - [184]
0.385953     53084.431776    0.110171    1   2   39.07   +       [9, 10, 11, 12, 14, 24, 28, 42]
0.342594     52938.986088    0.112999    2   2   29.89   -       [16, 19, 74, 75, 78, 84, 85] - [184]
0.280405     52807.403626    0.135596    3   2   26.30   -       [80, 81, 89, 91] - [184]
0.203603     52713.775850    0.112994    3   3   27.57   +       [6, 36, 44, 45]
0.199905     52623.793610    0.115819    5   2   28.59   -       [14, 19, 21, 23, 26] - [184]
0.185909     52543.282367    0.107347    6   2   55.45   -       [8, 10, 17, 24, 50] - [184]
0.150352     52463.650621    0.132768    6   3   99.24   -       [29, 57, 58] - [171]
0.147821     52392.307969    0.107349    7   3   29.28   -       [74, 78, 81, 82] - [152]
0.143550     52327.938809    0.104523    8   3   266.13      -       [3, 4, 10, 12, 14, 20] - [184]

[TIMER] Compute p: 25.596505
[TIMER] independence_estimate: 36.307801
[TIMER] mtv_query: 389.332130
[TIMER] Block weight: 121.273367
[TIMER] Cached query: 409.350854
[TIMER] Find best itemset: 739.276985
[TIMER] union_of_itemsets: 29.666200
[TIMER] Iterative scaling: 6.305821
[TIMER] Cummulative weight: 183.935984
[TIMER] Singletons of itemsets: 0.000108
[TIMER] Compute blocks: 0.050766
[TIMER] Build independent models: 6.339073
[COUNTER] Independence estimates: 2251605
[COUNTER] Block queries: 436958
[COUNTER] Total queries: 2688563
[COUNTER] Iterative scaling max iterations: 33
[COUNTER] Independent models: 3