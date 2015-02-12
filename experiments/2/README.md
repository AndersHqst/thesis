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

./main.py -f ../experiments/2/Stool_maxent_discretized_nodes_depth_6_040.dat -s 0.0 --debug -v -o ../experiments/2/ -k 10 -q 8 -H ../experiments/4/Stool_maxent_discretized_nodes_depth_6_040.headers
/Users/ahkj/pypy-2.4.0-osx64/site-packages/numpy/linalg/_umath_linalg.py:1322: UserWarning: no cffi linalg functions and no _umath_linalg_capi module, expect problems.
  warn('no cffi linalg functions and no _umath_linalg_capi module, expect problems.')
Found itemset (121.55 secs): [1, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 22, 23, 24, 25, 36, 37], score: 13697.915455, models: 1, Ci: [1], searched-nodes: 9275520
Found itemset (47.40 secs): [4, 5, 6, 7, 8, 17, 22], score: 13547.606001, models: 1, Ci: [2], searched-nodes: 5923372
Found itemset (35.39 secs): [9, 11, 16, 24, 28, 29, 31, 35], score: 13417.029371, models: 1, Ci: [3], searched-nodes: 5625849
Found itemset (16.90 secs): [11, 12, 13, 15, 16], score: 13297.272220, models: 1, Ci: [4], searched-nodes: 3580384
Found itemset (21.91 secs): [2, 5, 7, 8, 14, 18, 25], score: 13228.191755, models: 1, Ci: [5], searched-nodes: 3157251
Found itemset (34.64 secs): [8, 9, 10, 11, 16, 20, 26, 28, 29, 33], score: 13167.361029, models: 1, Ci: [6], searched-nodes: 2901831
Found itemset (71.31 secs): [12, 13, 14, 27, 32, 35, 36, 38], score: 13117.416999, models: 1, Ci: [7], searched-nodes: 1600269
Found itemset (174.91 secs): [0, 10, 12, 16, 24, 38], score: 13068.287729, models: 1, Ci: [8], searched-nodes: 1144233
Found itemset (0.01 secs): [19, 21], score: 12994.944741, models: 2, Ci: [8, 1], searched-nodes: 29
Found itemset (0.00 secs): [19, 21, 30, 34], score: 12989.992271, models: 2, Ci: [8, 2], searched-nodes: 29
39 items in 354 transactions

Model predictions:
query [1, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 22, 23, 24, 25, 36, 37] with fr 0.025424 query 0.025428
query [4, 5, 6, 7, 8, 17, 22] with fr 0.132768 query 0.132769
query [9, 11, 16, 24, 28, 29, 31, 35] with fr 0.101695 query 0.101700
query [11, 12, 13, 15, 16] with fr 0.189266 query 0.189271
query [2, 5, 7, 8, 14, 18, 25] with fr 0.098870 query 0.098873
query [8, 9, 10, 11, 16, 20, 26, 28, 29, 33] with fr 0.059322 query 0.059322
query [12, 13, 14, 27, 32, 35, 36, 38] with fr 0.062147 query 0.062153
query [0, 10, 12, 16, 24, 38] with fr 0.112994 query 0.112998
query [19, 21] with fr 0.115819 query 0.115819
query [19, 21, 30, 34] with fr 0.005650 query 0.005649

k=10, m=0, s=0.000000

MTV run time:  524.073338032

Summary: 
Heuristic    BIC score   p       |c|     models  Time    Relationship    Itemsets
x.xxxxxx     13790.247889    (No query)      0   0   0   +/-         I+seed
0.842574     13697.915455    0.025428    1   1   121.55      +       [1, 5, 8, 9, 10, 11, 12, 14, 15, 16, 17, 22, 23, 24, 25, 36, 37]
0.329195     13547.606001    0.132769    2   1   47.40   +       [4, 5, 6, 7, 8, 17, 22]
0.309910     13417.029371    0.101700    3   1   35.39   +       [9, 11, 16, 24, 28, 29, 31, 35]
0.211161     13297.272220    0.189271    4   1   16.90   +       [11, 12, 13, 15, 16]
0.152422     13228.191755    0.098873    5   1   21.91   +       [2, 5, 7, 8, 14, 18, 25]
0.147934     13167.361029    0.059322    6   1   34.64   +       [8, 9, 10, 11, 16, 20, 26, 28, 29, 33]
0.127812     13117.416999    0.062153    7   1   71.31   +       [12, 13, 14, 27, 32, 35, 36, 38]
0.098206     13068.287729    0.112998    8   1   174.91      +       [0, 10, 12, 16, 24, 38]
0.081384     12994.944741    0.115819    8   2   0.01    +       [19, 21]
0.020703     12989.992271    0.005649    8   2   0.00    +       [19, 21, 30, 34]

[TIMER] Compute p: 41.389570
[TIMER] independence_estimate: 16.207957
[TIMER] mtv_query: 310.282085
[TIMER] Block weight: 106.917807
[TIMER] Cached query: 344.070428
[TIMER] Find best itemset: 522.015660
[TIMER] union_of_itemsets: 5.982368
[TIMER] Iterative scaling: 1.991347
[TIMER] Cummulative weight: 117.706554
[TIMER] Singletons of itemsets: 0.000089
[TIMER] Compute blocks: 0.021017
[TIMER] Build independent models: 2.007397
[COUNTER] Independence estimates: 11340367
[COUNTER] Block queries: 2149713
[COUNTER] Total queries: 13490080
[COUNTER] Iterative scaling max iterations: 30
[COUNTER] Independent models: 2