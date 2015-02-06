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


101 items in 354 transactions

Model predictions:
query [16, 19, 20, 25, 26, 47] with fr 0.161017 query 0.161018
query [10, 11, 12, 14, 28, 42] with fr 0.158192 query 0.158188
query [16, 74, 75, 78, 84] with fr 0.158192 query 0.158189
query [16, 17, 19, 24, 91] with fr 0.161017 query 0.161005
query [19, 21, 23, 26] with fr 0.172316 query 0.172314
query [74, 80, 81, 91] with fr 0.152542 query 0.152550
query [8, 10, 17, 47] with fr 0.158192 query 0.158187
query [75, 78, 79, 85] with fr 0.197740 query 0.197743
query [9, 14, 24, 28, 42] with fr 0.163842 query 0.163841
query [17, 50, 89, 91] with fr 0.152542 query 0.152540

k=10, m=0, s=0.150000

MTV run time:  155.154405117

Summary: 
Heuristic    BIC score   p       |c|     models  Time    Itemsets
x.xxxxxx     19331.567309    (No query)      0   0   0   I+seed
0.348427     18591.343569    0.161018    1   1   6.29    [16, 19, 20, 25, 26, 47]
0.338312     17869.639300    0.158188    1   2   0.99    [10, 11, 12, 14, 28, 42]
0.200623     17324.894981    0.158189    2   2   0.87    [16, 74, 75, 78, 84]
0.174351     16842.934347    0.161005    3   2   0.86    [16, 17, 19, 24, 91]
0.150127     16415.026335    0.172314    4   2   0.79    [19, 21, 23, 26]
0.148622     16007.160725    0.152550    5   2   0.92    [74, 80, 81, 91]
0.131628     15620.468295    0.158187    7   1   1.65    [8, 10, 17, 47]
0.116151     15185.055710    0.197743    8   1   8.76    [75, 78, 79, 85]
0.111876     14841.056959    0.163841    9   1   28.76   [9, 14, 24, 28, 42]
0.109495     14506.501038    0.152540    10      1   105.17      [17, 50, 89, 91]

[TIMER] Compute p: 7.024513
[TIMER] independence_estimate: 0.431631
[TIMER] mtv_query: 104.808763
[TIMER] Block weight: 105.825682
[TIMER] Cached query: 105.015026
[TIMER] Find best itemset: 116.813908
[TIMER] union_of_itemsets: 0.519027
[TIMER] Iterative scaling: 38.115963
[TIMER] Cummulative weight: 28.725369
[TIMER] Singletons of itemsets: 0.000092
[TIMER] Compute blocks: 0.143832
[TIMER] Build independent models: 38.245670
[COUNTER] Independence estimates: 50101
[COUNTER] Block queries: 34192
[COUNTER] Total queries: 84293
[COUNTER] Iterative scaling max iterations: 30
[COUNTER] Independent models: 2