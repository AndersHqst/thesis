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
./main.py -f ../experiments/1/Stool_maxent_discretized_all_nodes.dat -m 2 -k 20 -o ../experiments/1/summary.dat --debug
notes:
    with -k 1 -m2 -s 0.05 running time is ~7 secs. These looks almost linear in k, ie 7*k for some small k
    with -k1 -m 3 -s 0.05 running time is 1 min to find first itemset

After data cleaning with removing discrete abundances that only occur below 0.05 times:
    we only have 201 nodes/attributes
    We can mine pairs at about 2 secs per results, ie time does not go much up as the
    summary size increases.

./main.py -f ../experiments/1/Stool_maxent_discretized_all_nodes.dat  -s 0.20 --debug -v -o ../experiments/1/ -k 10 -H ../experiments/1/Stool_maxent_discretized_all_nodes.headers --co-exclusion
/Users/ahkj/pypy-2.4.0-osx64/site-packages/numpy/linalg/_umath_linalg.py:1322: UserWarning: no cffi linalg functions and no _umath_linalg_capi module, expect problems.
  warn('no cffi linalg functions and no _umath_linalg_capi module, expect problems.')
Found itemset (346.00 secs): [2, 3, 16, 57, 89, 93, 99, 110, 126, 178, 209], score: 108541.336431, models: 1, Ci: [1], searched-nodes: 45935123
Found itemset (100.16 secs): [9, 33, 56, 98, 116, 148, 152, 166, 187], score: 107920.949921, models: 2, Ci: [1, 1], searched-nodes: 46007648
Found itemset (95.35 secs): [8, 35, 87, 151, 172, 301], score: 107180.537251, models: 3, Ci: [1, 1, 1], searched-nodes: 46060782
Found itemset (101.04 secs): [2, 3, 62, 78, 82, 85, 89, 164, 288], score: 106704.051369, models: 3, Ci: [1, 1, 2], searched-nodes: 46082948
Found itemset (96.10 secs): [96, 98, 103, 115, 166], score: 106116.350255, models: 3, Ci: [2, 1, 2], searched-nodes: 46101268
Found itemset (93.18 secs): [19, 27, 59, 91, 118, 155, 176], score: 105671.732089, models: 4, Ci: [2, 1, 2, 1], searched-nodes: 46100191
Found itemset (90.52 secs): [2, 3, 29, 63, 89, 122, 141, 153, 184, 209], score: 105237.583999, models: 4, Ci: [1, 1, 2, 3], searched-nodes: 46102517
Found itemset (93.78 secs): [28, 53, 102, 144], score: 104703.378578, models: 5, Ci: [3, 2, 1, 1, 1], searched-nodes: 46126182
Found itemset (89.09 secs): [74, 75, 130], score: 104137.365740, models: 6, Ci: [1, 1, 1, 2, 3, 1], searched-nodes: 46128785
Found itemset (89.62 secs): [64, 76, 101, 181], score: 103763.171633, models: 7, Ci: [1, 3, 2, 1, 1, 1, 1], searched-nodes: 46129139
402 items in 354 transactions

Model predictions:
query [2, 3, 16, 57, 89, 93, 99, 110, 126, 178, 209] with fr 0.223164 query 0.223164
query [9, 33, 56, 98, 116, 148, 152, 166, 187] with fr 0.231638 query 0.231619
query [8, 35, 87, 151, 172, 301] with fr 0.398305 query 0.398305
query [2, 3, 62, 78, 82, 85, 89, 164, 288] with fr 0.217514 query 0.217516
query [96, 98, 103, 115, 166] with fr 0.299435 query 0.299431
query [19, 27, 59, 91, 118, 155, 176] with fr 0.200565 query 0.200564
query [2, 3, 29, 63, 89, 122, 141, 153, 184, 209] with fr 0.203390 query 0.203411
query [28, 53, 102, 144] with fr 0.279661 query 0.279661
query [74, 75, 130] with fr 0.251412 query 0.251412
query [64, 76, 101, 181] with fr 0.262712 query 0.262712

k=10, m=0, s=0.200000

MTV run time:  1194.84517312

Summary: 
Heuristic    BIC score   p       |c|     models  Time    Relationship    Itemsets
x.xxxxxx     109409.389125   (No query)      0   0   0   +/-         I+seed
1.880357     108541.336431   0.223164    1   1   346.00      -       [2, 3, 16, 57, 89, 93, 99, 110, 126, 178] - [8]
1.306056     107920.949921   0.231619    1   2   100.16      +       [9, 33, 56, 98, 116, 148, 152, 166, 187]
1.082617     107180.537251   0.398305    1   3   95.35   -       [8, 35, 87, 151, 172] - [100]
0.978804     106704.051369   0.217516    2   3   101.04      -       [2, 3, 62, 78, 82, 85, 89, 164] - [87]
0.928785     106116.350255   0.299431    2   3   96.10   +       [96, 98, 103, 115, 166]
0.928019     105671.732089   0.200564    2   4   93.18   +       [19, 27, 59, 91, 118, 155, 176]
0.902592     105237.583999   0.203411    3   4   90.52   -       [2, 3, 29, 63, 89, 122, 141, 153, 184] - [8]
0.795695     104703.378578   0.279661    3   5   93.78   +       [28, 53, 102, 144]
0.706135     104137.365740   0.251412    3   6   89.09   +       [74, 75, 130]
0.604910     103763.171633   0.262712    3   7   89.62   +       [64, 76, 101, 181]

[TIMER] Compute p: 0.396245
[TIMER] independence_estimate: 104.393746
[TIMER] mtv_query: 139.911204
[TIMER] Block weight: 0.264943
[TIMER] Cached query: 158.324632
[TIMER] Find best itemset: 1194.370816
[TIMER] union_of_itemsets: 68.971274
[TIMER] Iterative scaling: 0.477122
[TIMER] Cummulative weight: 2.022984
[TIMER] Singletons of itemsets: 0.000136
[TIMER] Compute blocks: 0.005160
[TIMER] Build independent models: 0.448633
[COUNTER] Independence estimates: 2824126
[COUNTER] Block queries: 76931
[COUNTER] Total queries: 2901057
[COUNTER] Iterative scaling max iterations: 100
[COUNTER] Independent models: 7
