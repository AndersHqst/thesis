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


Found itemset (64.39 secs): [12, 13, 14, 15, 19, 31, 52, 103], score: 37316.304956, models: 1, Cs: [1]
Found itemset (8.53 secs): [6, 7, 8, 9, 10, 18, 21, 27], score: 37157.132238, models: 2, Cs: [1, 1]
Found itemset (7.67 secs): [12, 14, 39, 40, 43, 49, 50, 103], score: 37014.284348, models: 2, Cs: [1, 2]
Found itemset (7.84 secs): [45, 46, 51, 52, 103], score: 36883.793605, models: 2, Cs: [1, 3]
Found itemset (7.76 secs): [10, 14, 16, 17, 20, 31], score: 36782.398824, models: 1, Cs: [5]
Found itemset (23.76 secs): [3, 26, 28, 29], score: 36688.771047, models: 2, Cs: [5, 1]
Found itemset (7.74 secs): [1, 2, 7, 9, 10, 15, 103], score: 36612.458372, models: 2, Cs: [1, 6]
Found itemset (60.01 secs): [5, 7, 13, 30, 31], score: 36542.975785, models: 2, Cs: [1, 7]
Found itemset (145.01 secs): [39, 43, 46, 47], score: 36477.266425, models: 2, Cs: [1, 8]
Found itemset (393.83 secs): [22, 33, 34], score: 36404.544745, models: 3, Cs: [8, 1, 1]
110 items in 354 transactions

Model predictions:
query [12, 13, 14, 15, 19, 31, 52, 103] with fr 0.118644 query 0.118643
query [6, 7, 8, 9, 10, 18, 21, 27] with fr 0.110169 query 0.110168
query [12, 14, 39, 40, 43, 49, 50, 103] with fr 0.112994 query 0.112986
query [45, 46, 51, 52, 103] with fr 0.135593 query 0.135592
query [10, 14, 16, 17, 20, 31] with fr 0.112994 query 0.112996
query [3, 26, 28, 29] with fr 0.112994 query 0.112994
query [1, 2, 7, 9, 10, 15, 103] with fr 0.104520 query 0.104515
query [5, 7, 13, 30, 31] with fr 0.104520 query 0.104515
query [39, 43, 46, 47] with fr 0.107345 query 0.107348
query [22, 33, 34] with fr 0.135593 query 0.135593

k=10, m=0, s=0.100000

MTV run time:  726.546221018

Summary: 
Heuristic    BIC score   p       |c|     models  Time    Relationship    Itemsets
x.xxxxxx     37495.344980    (No query)      0   0   0   +/-         I+seed
0.428678     37316.304956    0.118643    1   1   64.39   -       [12, 13, 14, 15, 19, 31, 52] - [48]
0.385953     37157.132238    0.110168    1   2   8.53    +       [6, 7, 8, 9, 10, 18, 21, 27]
0.335821     37014.284348    0.112986    2   2   7.67    -       [12, 14, 39, 40, 43, 49, 50] - [48]
0.277734     36883.793605    0.135592    3   2   7.84    -       [45, 46, 51, 52] - [48]
0.233937     36782.398824    0.112996    5   1   7.76    +       [10, 14, 16, 17, 20, 31]
0.203603     36688.771047    0.112994    5   2   23.76   +       [3, 26, 28, 29]
0.175825     36612.458372    0.104515    6   2   7.74    -       [1, 2, 7, 9, 10, 15] - [48]
0.156575     36542.975785    0.104515    7   2   60.01   +       [5, 7, 13, 30, 31]
0.134479     36477.266425    0.107348    8   2   145.01      +       [39, 43, 46, 47]
0.132408     36404.544745    0.135593    8   3   393.83      +       [22, 33, 34]

[TIMER] Compute p: 42.155339
[TIMER] independence_estimate: 3.956882
[TIMER] mtv_query: 596.286206
[TIMER] Block weight: 296.383675
[TIMER] Cached query: 600.991288
[TIMER] Find best itemset: 721.698202
[TIMER] union_of_itemsets: 6.837795
[TIMER] Iterative scaling: 4.810292
[TIMER] Cummulative weight: 252.112358
[TIMER] Singletons of itemsets: 0.000097
[TIMER] Compute blocks: 0.038839
[TIMER] Build independent models: 4.836272
[COUNTER] Independence estimates: 571792
[COUNTER] Block queries: 457676
[COUNTER] Total queries: 1029468
[COUNTER] Iterative scaling max iterations: 25
[COUNTER] Independent models: 3