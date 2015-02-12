Experiment with all nodes in phylogenetic tree.

IMPORTANT: This experiment can only be executed on the hqst/decimalSimple branch. The size of the 
problem will cause float precision problems resulting in very small values becoming 0. On hqst/decimalSimple
this is taken care of with the decimal library, which will make computation considerably slower.

Setup:
    Sample abundance counts are made relative to the sample.
    Data is discretized with the maxent discretization.


Questions:
    We can only mine pairs, as sample space is 2**354.
        How 'heavy' is it to mine e.g. triplets?

    Can we even do this? I.e. can we make the BIC score converge.
    What is the summary?        
        Only stuff in same lineage?
        Do we get any of the Faust results?
        Can we query the Faust results?
        Does this make sense biologically? 
            - Talk to bio about this.
        Do the patterns overlap?
            Build grap to easily visualize this.


Report:
    Write about results based on above questions.
    Create scatter plots for summary, with discretization lines. We can do this because of only mining pairs
        Put representative plot.


1 attempt:

Cleaning:
tree nodes before:  315
tree leafs before:  186
discrete dataset cleaning, removed bacteria:  196
Final number of attributes:  118
    

./main.py -f ../experiments/1/Stool_maxent_discretized_all_nodes_020.dat  -s 0.2 --debug -v -o ../experiments/1/ -k 20 -q 8 -H ../experiments/1/Stool_maxent_discretized_all_nodes_020.headers --co-exclusion
/Users/ahkj/pypy-2.4.0-osx64/site-packages/numpy/linalg/_umath_linalg.py:1322: UserWarning: no cffi linalg functions and no _umath_linalg_capi module, expect problems.
  warn('no cffi linalg functions and no _umath_linalg_capi module, expect problems.')
Found itemset (159.95 secs): [1, 2, 9, 29, 52, 54, 59, 64, 73, 104, 168], score: 79504.214306, models: 1, Ci: [1], searched-nodes: 8746520
Found itemset (23.98 secs): [6, 20, 28, 58, 67, 85, 89, 98, 111], score: 78883.827796, models: 2, Ci: [1, 1], searched-nodes: 8757804
Found itemset (20.44 secs): [5, 21, 50, 88, 101], score: 78147.113409, models: 3, Ci: [1, 1, 1], searched-nodes: 8768346
Found itemset (22.45 secs): [1, 2, 18, 34, 52, 70, 82, 90, 109], score: 77690.859817, models: 3, Ci: [1, 1, 2], searched-nodes: 8770501
Found itemset (22.14 secs): [57, 58, 62, 66, 98], score: 77103.158703, models: 3, Ci: [2, 1, 2], searched-nodes: 8772166
Found itemset (21.76 secs): [11, 16, 31, 53, 68, 92, 102], score: 76658.540538, models: 4, Ci: [2, 1, 2, 1], searched-nodes: 8772326
Found itemset (20.13 secs): [1, 2, 33, 43, 46, 49, 52, 97, 219], score: 76234.662888, models: 4, Ci: [1, 1, 2, 3], searched-nodes: 8773302
Found itemset (23.46 secs): [17, 27, 61, 83], score: 75700.457467, models: 5, Ci: [3, 2, 1, 1, 1], searched-nodes: 8781981
Found itemset (21.67 secs): [40, 41, 75], score: 75134.444629, models: 6, Ci: [1, 1, 1, 2, 3, 1], searched-nodes: 8782594
Found itemset (21.63 secs): [35, 42, 60, 106], score: 74760.250521, models: 7, Ci: [1, 3, 2, 1, 1, 1, 1], searched-nodes: 8783691
Found itemset (22.26 secs): [1, 2, 32, 48, 52, 70, 86, 100], score: 74480.315231, models: 7, Ci: [1, 1, 1, 1, 2, 1, 4], searched-nodes: 8784078
Found itemset (31.25 secs): [1, 2, 9, 20, 30, 52, 111, 115, 168], score: 74236.240724, models: 6, Ci: [1, 1, 1, 1, 1, 7], searched-nodes: 8787227
Found itemset (231.03 secs): [1, 2, 14, 69, 76, 139], score: 74011.968409, models: 6, Ci: [1, 1, 1, 1, 1, 8], searched-nodes: 8784323
Found itemset (7.81 secs): [13, 25, 47, 51, 78], score: 73838.998958, models: 7, Ci: [8, 1, 1, 1, 1, 1, 1], searched-nodes: 650286
Found itemset (1.26 secs): [5, 15, 21, 50, 81, 170], score: 73644.663947, models: 7, Ci: [1, 1, 1, 1, 1, 8, 2], searched-nodes: 650225
Found itemset (1.30 secs): [4, 25, 44, 74], score: 73476.209827, models: 7, Ci: [2, 8, 1, 1, 1, 1, 2], searched-nodes: 650284
Found itemset (1.34 secs): [5, 11, 21, 50, 53, 68, 120], score: 73322.516293, models: 6, Ci: [2, 1, 1, 1, 8, 4], searched-nodes: 650249
Found itemset (1.33 secs): [19, 79], score: 73075.307583, models: 7, Ci: [4, 8, 1, 1, 1, 2, 1], searched-nodes: 650241
Found itemset (1.76 secs): [31, 39, 60, 102], score: 72924.508517, models: 6, Ci: [1, 2, 1, 1, 8, 6], searched-nodes: 650090
Found itemset (2.11 secs): [112, 114], score: 72665.807932, models: 7, Ci: [6, 8, 1, 1, 2, 1, 1], searched-nodes: 650090
236 items in 354 transactions

Model predictions:
query [1, 2, 9, 29, 52, 54, 59, 64, 73, 104, 168] with fr 0.223164 query 0.223113
query [6, 20, 28, 58, 67, 85, 89, 98, 111] with fr 0.231638 query 0.231609
query [5, 21, 50, 88, 101] with fr 0.401130 query 0.401148
query [1, 2, 18, 34, 52, 70, 82, 90, 109] with fr 0.211864 query 0.211868
query [57, 58, 62, 66, 98] with fr 0.299435 query 0.299435
query [11, 16, 31, 53, 68, 92, 102] with fr 0.200565 query 0.200571
query [1, 2, 33, 43, 46, 49, 52, 97, 219] with fr 0.209040 query 0.209011
query [17, 27, 61, 83] with fr 0.279661 query 0.279661
query [40, 41, 75] with fr 0.251412 query 0.251412
query [35, 42, 60, 106] with fr 0.262712 query 0.262710
query [1, 2, 32, 48, 52, 70, 86, 100] with fr 0.211864 query 0.211849
query [1, 2, 9, 20, 30, 52, 111, 115, 168] with fr 0.203390 query 0.203348
query [1, 2, 14, 69, 76, 139] with fr 0.214689 query 0.214657
query [13, 25, 47, 51, 78] with fr 0.206215 query 0.206215
query [5, 15, 21, 50, 81, 170] with fr 0.251412 query 0.251391
query [4, 25, 44, 74] with fr 0.209040 query 0.209039
query [5, 11, 21, 50, 53, 68, 120] with fr 0.220339 query 0.220305
query [19, 79] with fr 0.223164 query 0.223164
query [31, 39, 60, 102] with fr 0.234463 query 0.234446
query [112, 114] with fr 0.285311 query 0.285311

k=20, m=0, s=0.200000

MTV run time:  659.244479179

Summary: 
Heuristic    BIC score   p       |c|     models  Time    Relationship    Itemsets
x.xxxxxx     80372.267000    (No query)      0   0   0   +/-         I+seed
1.880357     79504.214306    0.223113    1   1   159.95      -       [1, 2, 9, 29, 52, 54, 59, 64, 73, 104] - [168]
1.306056     78883.827796    0.231609    1   2   23.98   +       [6, 20, 28, 58, 67, 85, 89, 98, 111]
1.061472     78147.113409    0.401148    1   3   20.44   +       [5, 21, 50, 88, 101]
0.944478     77690.859817    0.211868    2   3   22.45   +       [1, 2, 18, 34, 52, 70, 82, 90, 109]
0.928787     77103.158703    0.299435    2   3   22.14   +       [57, 58, 62, 66, 98]
0.928019     76658.540538    0.200571    2   4   21.76   +       [11, 16, 31, 53, 68, 92, 102]
0.885554     76234.662888    0.209011    3   4   20.13   -       [1, 2, 33, 43, 46, 49, 52, 97] - [219]
0.795695     75700.457467    0.279661    3   5   23.46   +       [17, 27, 61, 83]
0.706135     75134.444629    0.251412    3   6   21.67   +       [40, 41, 75]
0.604910     74760.250521    0.262710    3   7   21.63   +       [35, 42, 60, 106]
0.539247     74480.315231    0.211849    4   7   22.26   +       [1, 2, 32, 48, 52, 70, 86, 100]
0.450653     74236.240724    0.203348    7   6   31.25   -       [1, 2, 9, 20, 30, 52, 111, 115] - [168]
0.434873     74011.968409    0.214657    8   6   231.03      -       [1, 2, 14, 69, 76] - [139]
0.333247     73838.998958    0.206215    8   7   7.81    +       [13, 25, 47, 51, 78]
0.325617     73644.663947    0.251391    8   7   1.26    -       [5, 15, 21, 50, 81] - [170]
0.293710     73476.209827    0.209039    8   7   1.30    +       [4, 25, 44, 74]
0.252581     73322.516293    0.220305    8   6   1.34    -       [5, 11, 21, 50, 53, 68] - [120]
0.247358     73075.307583    0.223164    8   7   1.33    +       [19, 79]
0.236667     72924.508517    0.234446    8   6   1.76    +       [31, 39, 60, 102]
0.233325     72665.807932    0.285311    8   7   2.11    +       [112, 114]

[TIMER] Compute p: 14.573552
[TIMER] independence_estimate: 17.287486
[TIMER] mtv_query: 230.514017
[TIMER] Block weight: 74.365764
[TIMER] Cached query: 236.268874
[TIMER] Find best itemset: 637.845868
[TIMER] union_of_itemsets: 16.778923
[TIMER] Iterative scaling: 21.169297
[TIMER] Cummulative weight: 130.930555
[TIMER] Singletons of itemsets: 0.000230
[TIMER] Compute blocks: 0.045537
[TIMER] Build independent models: 21.193422
[COUNTER] Independence estimates: 891958
[COUNTER] Block queries: 279416
[COUNTER] Total queries: 1171374
[COUNTER] Iterative scaling max iterations: 100
[COUNTER] Independent models: 7