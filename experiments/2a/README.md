Experiment with only bacteria at the genus level. Using support 0, and do not include negated attributes


Setup:
    Sample abundance counts are made relative to the sample.
    Data is discretized with the maxent discretization.
    Remove 0.40 threshold in preprocessing.

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

./main.py -f ../experiments/4/Stool_maxent_discretized_nodes_depth_6_005.dat -s 0.0 --debug -v -o ../experiments/2a/ -k 10 -H ../experiments/4/Stool_maxent_discretized_nodes_depth_6_005.headers -q 7 -m 4
/Users/ahkj/pypy-2.4.0-osx64/site-packages/numpy/linalg/_umath_linalg.py:1322: UserWarning: no cffi linalg functions and no _umath_linalg_capi module, expect problems.
  warn('no cffi linalg functions and no _umath_linalg_capi module, expect problems.')
Found itemset (255.63 secs): [16, 19, 20, 26], score: 26567.288897, models: 1, Ci: [1], searched-nodes: 3374409
Found itemset (107.97 secs): [6, 36, 44, 45], score: 26473.661121, models: 2, Ci: [1, 1], searched-nodes: 3375935
Found itemset (102.99 secs): [10, 12, 14, 28], score: 26359.730361, models: 3, Ci: [1, 1, 1], searched-nodes: 3376105
Found itemset (108.69 secs): [80, 81, 89, 91], score: 26267.273905, models: 4, Ci: [1, 1, 1, 1], searched-nodes: 3537199
Found itemset (114.69 secs): [74, 78, 81, 82], score: 26187.525808, models: 4, Ci: [1, 1, 1, 2], searched-nodes: 3714260
Found itemset (94.62 secs): [9, 11, 14, 42], score: 26096.061187, models: 4, Ci: [2, 1, 1, 2], searched-nodes: 3714751
Found itemset (92.26 secs): [23, 26, 75, 78], score: 26010.830558, models: 3, Ci: [2, 1, 4], searched-nodes: 3715686
Found itemset (90.01 secs): [16, 17, 47, 91], score: 25923.136943, models: 3, Ci: [1, 2, 5], searched-nodes: 3716694
Found itemset (89.17 secs): [6, 29, 57, 58], score: 25855.285737, models: 3, Ci: [5, 2, 2], searched-nodes: 3714134
Found itemset (85.03 secs): [8, 10, 17, 24], score: 25775.289775, models: 2, Ci: [2, 8], searched-nodes: 3714189
101 items in 354 transactions

Model predictions:
query [16, 19, 20, 26] with fr 0.245763 query 0.245767
query [6, 36, 44, 45] with fr 0.112994 query 0.112994
query [10, 12, 14, 28] with fr 0.223164 query 0.223163
query [80, 81, 89, 91] with fr 0.138418 query 0.138418
query [74, 78, 81, 82] with fr 0.107345 query 0.107345
query [9, 11, 14, 42] with fr 0.206215 query 0.206215
query [23, 26, 75, 78] with fr 0.163842 query 0.163842
query [16, 17, 47, 91] with fr 0.203390 query 0.203390
query [6, 29, 57, 58] with fr 0.087571 query 0.087568
query [8, 10, 17, 24] with fr 0.163842 query 0.163846

k=10, m=4, s=0.000000

MTV run time:  1141.34649205

Summary: 
Heuristic    BIC score   p       |c|     models  Time    U       Itemsets
x.xxxxxx     26714.863022    (No query)      0   0   0   >1<         I+seed
0.248785     26567.288897    0.245767    1   1   255.63      22.170926   [16, 19, 20, 26]
0.203603     26473.661121    0.112994    1   2   107.97      26.768555   [6, 36, 44, 45]
0.199083     26359.730361    0.223163    1   3   102.99      15.342390   [10, 12, 14, 28]
0.187732     26267.273905    0.138418    1   4   108.69      19.384438   [80, 81, 89, 91]
0.169989     26187.525808    0.107345    2   4   114.69      22.550973   [74, 78, 81, 82]
0.164583     26096.061187    0.206215    2   4   94.62   11.716639   [9, 11, 14, 42]
0.163881     26010.830558    0.163842    4   3   92.26   13.636587   [23, 26, 75, 78]
0.158601     25923.136943    0.203390    5   3   90.01   11.162885   [16, 17, 47, 91]
0.155840     25855.285737    0.087568    5   3   89.17   21.746467   [6, 29, 57, 58]
0.154531     25775.289775    0.163846    8   2   85.03   12.301172   [8, 10, 17, 24]

[TIMER] Compute p: 0.354905
[TIMER] independence_estimate: 227.935663
[TIMER] mtv_query: 401.262907
[TIMER] Block weight: 1.173444
[TIMER] Cached query: 560.958922
[TIMER] Find best itemset: 1139.249766
[TIMER] union_of_itemsets: 100.779223
[TIMER] Iterative scaling: 1.781923
[TIMER] Cummulative weight: 1.066465
[TIMER] Singletons of itemsets: 0.000095
[TIMER] Compute blocks: 0.025066
[TIMER] Build independent models: 1.793892
[COUNTER] Independence estimates: 34893105
[COUNTER] Block queries: 7097
[COUNTER] Total queries: 34900202
[COUNTER] Iterative scaling max iterations: 21
[COUNTER] Independent models: 4