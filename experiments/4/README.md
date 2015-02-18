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

./main.py -f ../experiments/4/Stool_maxent_discretized_nodes_depth_6_010.dat -s 0.1 --debug -v -o ../experiments/4/ -k 10 -H ../experiments/4/Stool_maxent_discretized_nodes_depth_6_010.headers --add-negated
/Users/ahkj/pypy-2.4.0-osx64/site-packages/numpy/linalg/_umath_linalg.py:1322: UserWarning: no cffi linalg functions and no _umath_linalg_capi module, expect problems.
  warn('no cffi linalg functions and no _umath_linalg_capi module, expect problems.')
Found itemset (480.34 secs): [13, 14, 16, 17, 22, 23, 41, 73, 147], score: 47489.438932, models: 1, Ci: [1], searched-nodes: 34208302
Found itemset (95.90 secs): [7, 8, 9, 10, 11, 21, 25, 36], score: 47330.266214, models: 2, Ci: [1, 1], searched-nodes: 34208298
Found itemset (81.84 secs): [13, 16, 59, 60, 63, 69, 70, 147], score: 47184.820525, models: 2, Ci: [1, 2], searched-nodes: 34208254
Found itemset (87.16 secs): [65, 66, 71, 73, 147], score: 47053.238064, models: 2, Ci: [1, 3], searched-nodes: 34208249
Found itemset (86.17 secs): [4, 32, 38, 39], score: 46959.610287, models: 3, Ci: [3, 1, 1], searched-nodes: 34208178
Found itemset (84.77 secs): [11, 16, 18, 20, 23, 147], score: 46869.628047, models: 2, Ci: [1, 5], searched-nodes: 34208161
Found itemset (106.45 secs): [6, 8, 14, 21, 43, 147], score: 46789.116805, models: 2, Ci: [1, 6], searched-nodes: 34208154
Found itemset (144.92 secs): [26, 47, 48, 136], score: 46709.485059, models: 3, Ci: [6, 1, 1], searched-nodes: 34208118
Found itemset (89.02 secs): [2, 3, 8, 10, 11, 17, 147], score: 46645.112607, models: 3, Ci: [1, 1, 7], searched-nodes: 34208109
Found itemset (282.93 secs): [14, 16, 40, 41, 78, 147], score: 46579.654929, models: 3, Ci: [1, 1, 8], searched-nodes: 34208065
158 items in 354 transactions

Model predictions:
query [13, 14, 16, 17, 22, 23, 41, 73, 147] with fr 0.104520 query 0.104523
query [7, 8, 9, 10, 11, 21, 25, 36] with fr 0.110169 query 0.110167
query [13, 16, 59, 60, 63, 69, 70, 147] with fr 0.112994 query 0.112995
query [65, 66, 71, 73, 147] with fr 0.135593 query 0.135598
query [4, 32, 38, 39] with fr 0.112994 query 0.112994
query [11, 16, 18, 20, 23, 147] with fr 0.115819 query 0.115827
query [6, 8, 14, 21, 43, 147] with fr 0.107345 query 0.107347
query [26, 47, 48, 136] with fr 0.132768 query 0.132768
query [2, 3, 8, 10, 11, 17, 147] with fr 0.104520 query 0.104519
query [14, 16, 40, 41, 78, 147] with fr 0.107345 query 0.107345

k=10, m=0, s=0.100000

MTV run time:  1545.06706595

Summary: 
Heuristic    BIC score   p       |c|     models  Time    U       Itemsets
x.xxxxxx     47675.560482    (No query)      0   0   0   >1<         I+seed
0.460042     47489.438932    0.104523    1   1   480.34      33.703004   [13, 14, 16, 17, 22, 23, 41, 73] - [147]
0.385953     47330.266214    0.110167    1   2   95.90   53.463529   [7, 8, 9, 10, 11, 21, 25, 36]
0.342594     47184.820525    0.112995    2   2   81.84   60.916493   [13, 16, 59, 60, 63, 69, 70] - [147]
0.280406     47053.238064    0.135598    3   2   87.16   40.227947   [65, 66, 71, 73] - [147]
0.203603     46959.610287    0.112994    3   3   86.17   26.764591   [4, 32, 38, 39]
0.199904     46869.628047    0.115827    5   2   84.77   17.651754   [11, 16, 18, 20, 23] - [147]
0.185909     46789.116805    0.107347    6   2   106.45      15.424504   [6, 8, 14, 21, 43] - [147]
0.150352     46709.485059    0.132768    6   3   144.92      18.738639   [26, 47, 48] - [136]
0.143567     46645.112607    0.104519    7   3   89.02   14.581164   [2, 3, 8, 10, 11, 17] - [147]
0.138511     46579.654929    0.107345    8   3   282.93      15.462481   [14, 16, 40, 41, 78] - [147]

[TIMER] Compute p: 22.488985
[TIMER] independence_estimate: 45.253439
[TIMER] mtv_query: 360.721742
[TIMER] Block weight: 108.524761
[TIMER] Cached query: 387.504329
[TIMER] Find best itemset: 1534.093432
[TIMER] union_of_itemsets: 45.254550
[TIMER] Iterative scaling: 5.349499
[TIMER] Cummulative weight: 144.184626
[TIMER] Singletons of itemsets: 0.000111
[TIMER] Compute blocks: 0.062029
[TIMER] Build independent models: 5.396122
[COUNTER] Independence estimates: 3570985
[COUNTER] Block queries: 371837
[COUNTER] Total queries: 3942822
[COUNTER] Iterative scaling max iterations: 28
[COUNTER] Independent models: 3