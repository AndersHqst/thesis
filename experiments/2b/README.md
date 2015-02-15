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

./main.py -f ../experiments/4/Stool_maxent_discretized_nodes_depth_6_005.dat -s 0.0 --debug -v -o ../experiments/2b/ -k 10 -H ../experiments/4/Stool_maxent_discretized_nodes_depth_6_005.headers -q 7 -m 4
/Users/ahkj/pypy-2.4.0-osx64/site-packages/numpy/linalg/_umath_linalg.py:1322: UserWarning: no cffi linalg functions and no _umath_linalg_capi module, expect problems.
  warn('no cffi linalg functions and no _umath_linalg_capi module, expect problems.')


Found itemset (51.72 secs): [19, 83], score: 26638.014152, models: 1, Ci: [1], searched-nodes: 742801
Found itemset (22.13 secs): [25, 81, 83], score: 26603.627974, models: 1, Ci: [2], searched-nodes: 743497
Found itemset (21.87 secs): [31, 35], score: 26530.284986, models: 2, Ci: [2, 1], searched-nodes: 757454
Found itemset (20.02 secs): [33, 80, 83], score: 26492.104023, models: 2, Ci: [1, 3], searched-nodes: 765271
Found itemset (23.79 secs): [14, 17, 79, 83], score: 26468.468616, models: 2, Ci: [1, 4], searched-nodes: 834998
Found itemset (21.70 secs): [83, 89], score: 26425.478994, models: 2, Ci: [1, 5], searched-nodes: 886997
Found itemset (20.71 secs): [63, 65], score: 26382.921293, models: 3, Ci: [5, 1, 1], searched-nodes: 899469
Found itemset (19.14 secs): [0, 26, 83], score: 26362.783316, models: 3, Ci: [1, 1, 6], searched-nodes: 899228
Found itemset (32.61 secs): [23, 83], score: 26325.971393, models: 3, Ci: [1, 1, 7], searched-nodes: 1077286
Found itemset (46.39 secs): [9, 16, 32, 35], score: 26317.750193, models: 3, Ci: [7, 1, 2], searched-nodes: 786606
101 items in 354 transactions

Model predictions:
query [19, 83] with fr 0.112994 query 0.112994
query [25, 81, 83] with fr 0.005650 query 0.005650
query [31, 35] with fr 0.115819 query 0.115823
query [33, 80, 83] with fr 0.031073 query 0.031073
query [14, 17, 79, 83] with fr 0.005650 query 0.005650
query [83, 89] with fr 0.067797 query 0.067796
query [63, 65] with fr 0.098870 query 0.098870
query [0, 26, 83] with fr 0.002825 query 0.002825
query [23, 83] with fr 0.070621 query 0.070619
query [9, 16, 32, 35] with fr 0.000000 query 0.000000

k=10, m=4, s=0.000000

MTV run time:  280.128067017

Summary: 
Heuristic    BIC score   p       |c|     models  Time    U       Itemsets
x.xxxxxx     26714.863022    (No query)      0   0   0   >1<         I+seed
0.085247     26638.014152    0.112994    1   1   51.72   0.085270    [19, 83]
0.083449     26603.627974    0.005650    2   1   22.13   0.042457    [25, 81, 83]
0.081384     26530.284986    0.115823    2   2   21.87   0.090907    [31, 35]
0.079251     26492.104023    0.031073    3   2   20.02   0.125515    [33, 80, 83]
0.064860     26468.468616    0.005650    4   2   23.79   0.061201    [14, 17, 79, 83]
0.062798     26425.478994    0.067796    5   2   21.70   0.138515    [83, 89]
0.056079     26382.921293    0.098870    5   3   20.71   0.157495    [63, 65]
0.055182     26362.783316    0.002825    6   3   19.14   0.037445    [0, 26, 83]
0.054592     26325.971393    0.070619    7   3   32.61   0.159010    [23, 83]
0.031935     26317.750193    0.000000    7   3   46.39   0.000000    [9, 16, 32, 35]

[TIMER] Compute p: 0.189498
[TIMER] independence_estimate: 66.036678
[TIMER] mtv_query: 99.887002
[TIMER] Block weight: 0.364783
[TIMER] Cached query: 127.447237
[TIMER] Find best itemset: 279.362450
[TIMER] union_of_itemsets: 23.406797
[TIMER] Iterative scaling: 0.707943
[TIMER] Cummulative weight: 0.606743
[TIMER] Singletons of itemsets: 0.000090
[TIMER] Compute blocks: 0.023658
[TIMER] Build independent models: 0.717349
[COUNTER] Independence estimates: 9754389
[COUNTER] Block queries: 4807
[COUNTER] Total queries: 9759196
[COUNTER] Iterative scaling max iterations: 31
[COUNTER] Independent models: 3