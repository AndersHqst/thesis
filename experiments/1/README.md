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


201 items in 354 transactions

Model predictions:
query [74, 75] with fr 0.251412 query 0.248600
query [74, 130] with fr 0.251412 query 0.247345
query [128, 171] with fr 0.197740 query 0.197740
query [92, 189] with fr 0.192090 query 0.192577
query [30, 135] with fr 0.223164 query 0.223079
query [10, 198] with fr 0.194915 query 0.195178
query [96, 115] with fr 0.364407 query 0.366768
query [96, 103] with fr 0.364407 query 0.364407
query [14, 73] with fr 0.158192 query 0.158155
query [51, 97] with fr 0.155367 query 0.154611
query [5, 72] with fr 0.152542 query 0.153782
query [161, 188] with fr 0.152542 query 0.151218
query [76, 181] with fr 0.389831 query 0.389831
query [5, 23] with fr 0.152542 query 0.156050
query [59, 176] with fr 0.403955 query 0.405440
query [72, 161] with fr 0.152542 query 0.156359
query [53, 102] with fr 0.409605 query 0.406960
query [37, 113] with fr 0.138418 query 0.136767
query [192, 194] with fr 0.285311 query 0.286274
query [93, 99] with fr 0.440678 query 0.427421
query [110, 178] with fr 0.440678 query 0.436029
query [93, 110] with fr 0.440678 query 0.431399
query [114, 191] with fr 0.115819 query 0.117886
query [129, 174] with fr 0.115819 query 0.120121
query [6, 145] with fr 0.115819 query 0.116841
query [6, 169] with fr 0.115819 query 0.115819
query [114, 174] with fr 0.115819 query 0.115819
query [71, 108] with fr 0.110169 query 0.110169
query [47, 55] with fr 0.129944 query 0.129944
query [99, 126] with fr 0.440678 query 0.436803
query [35, 87] with fr 0.500000 query 0.494497
query [33, 187] with fr 0.500000 query 0.495640
query [151, 172] with fr 0.500000 query 0.499338
query [98, 166] with fr 0.500000 query 0.499330
query [63, 141] with fr 0.500000 query 0.497388
query [53, 144] with fr 0.372881 query 0.370317
query [63, 184] with fr 0.500000 query 0.492242
query [14, 50] with fr 0.135593 query 0.135593
query [2, 3] with fr 0.497175 query 0.496844
query [61, 170] with fr 0.497175 query 0.497175
query [69, 138] with fr 0.093220 query 0.093220
query [167, 175] with fr 0.090395 query 0.091214
query [19, 118] with fr 0.494350 query 0.493877
query [37, 190] with fr 0.118644 query 0.115577
query [8, 35] with fr 0.494350 query 0.487129
query [26, 140] with fr 0.491525 query 0.491525
query [22, 132] with fr 0.491525 query 0.491525
query [2, 89] with fr 0.491525 query 0.491849
query [34, 185] with fr 0.118644 query 0.118239
query [92, 130] with fr 0.194915 query 0.191887
query [9, 152] with fr 0.488701 query 0.488562
query [64, 76] with fr 0.319209 query 0.321892
query [77, 159] with fr 0.073446 query 0.073446
query [59, 155] with fr 0.330508 query 0.328191
query [56, 116] with fr 0.480226 query 0.480177
query [46, 107] with fr 0.064972 query 0.064972
query [142, 190] with fr 0.093220 query 0.091844
query [121, 133] with fr 0.169492 query 0.168820
query [19, 91] with fr 0.474576 query 0.476989
query [28, 144] with fr 0.279661 query 0.281604
query [48, 112] with fr 0.059322 query 0.058302
query [13, 90] with fr 0.059322 query 0.057791
query [39, 100] with fr 0.059322 query 0.059259
query [17, 48] with fr 0.059322 query 0.056301
query [13, 17] with fr 0.059322 query 0.057412
query [51, 60] with fr 0.104520 query 0.102592
query [15, 117] with fr 0.053672 query 0.053161
query [15, 39] with fr 0.053672 query 0.054721
query [1, 11] with fr 0.432203 query 0.432218
query [146, 185] with fr 0.090395 query 0.090395
query [9, 56] with fr 0.454802 query 0.455133
query [52, 133] with fr 0.144068 query 0.144068
query [27, 118] with fr 0.454802 query 0.456547
query [8, 16] with fr 0.081921 query 0.081908
query [62, 78] with fr 0.449153 query 0.449153
query [7, 127] with fr 0.443503 query 0.443808
query [122, 153] with fr 0.443503 query 0.443503
query [10, 179] with fr 0.200565 query 0.200565
query [32, 199] with fr 0.070621 query 0.070880
query [36, 97] with fr 0.076271 query 0.075592
query [3, 16] with fr 0.432203 query 0.432135
query [24, 192] with fr 0.146893 query 0.146893
query [137, 176] with fr 0.217514 query 0.217649
query [33, 148] with fr 0.429379 query 0.430352
query [164, 172] with fr 0.101695 query 0.102098
query [67, 135] with fr 0.172316 query 0.173960
query [35, 57] with fr 0.104520 query 0.104504
query [79, 127] with fr 0.296610 query 0.296623
query [29, 141] with fr 0.420904 query 0.423028
query [98, 187] with fr 0.418079 query 0.418102
query [83, 134] with fr 0.415254 query 0.415254
query [32, 86] with fr 0.053672 query 0.053672
query [160, 181] with fr 0.175141 query 0.176453
query [35, 82] with fr 0.110169 query 0.108966
query [21, 88] with fr 0.412429 query 0.412418
query [89, 172] with fr 0.110169 query 0.110241
query [11, 68] with fr 0.305085 query 0.305085
query [130, 167] with fr 0.090395 query 0.088772
query [21, 43] with fr 0.403955 query 0.403955
query [42, 79] with fr 0.161017 query 0.161017

k=100, m=2, s=0.050000

MTV run time:  1334.56451988

Summary: 
Heuristic    BIC score   p       |c|     models  Time    Itemsets
x.xxxxxx     40518.023230    (No query)      0   0   0   I+seed
0.258570     39074.001363    0.248600    1   1   2.19    [74, 75]
0.256374     37719.112761    0.247345    2   1   1.49    [74, 130]
0.253540     36569.894888    0.197740    2   2   1.18    [128, 171]
0.249014     35502.325456    0.192577    2   3   1.17    [92, 189]
0.247358     34339.961330    0.223079    2   4   1.15    [30, 135]
0.246283     33295.161562    0.195178    2   5   1.34    [10, 198]
0.245794     31225.472539    0.366768    2   6   1.31    [96, 115]
0.243293     29261.774895    0.364407    2   6   1.19    [96, 103]
0.242473     28330.655881    0.158155    2   7   1.03    [14, 73]
0.241374     27415.179937    0.154611    2   8   1.23    [51, 97]
0.240228     26515.358414    0.153782    2   9   1.29    [5, 72]
0.240228     25615.536891    0.151218    2   10      1.06    [161, 188]
0.240036     23402.691014    0.389831    2   11      1.11    [76, 181]
0.238602     22549.957268    0.156050    2   11      1.40    [5, 23]
0.236503     20257.020589    0.405440    2   12      1.43    [59, 176]
0.235393     19333.620211    0.156359    4   11      1.58    [72, 161]
0.235029     17008.523996    0.406960    4   12      1.41    [53, 102]
0.233750     16187.165585    0.136767    4   13      1.23    [37, 113]
0.233325     14820.060985    0.286274    4   14      1.46    [192, 194]
0.226349     12316.691508    0.427421    4   15      1.71    [93, 99]
0.226349     9813.322031     0.436029    4   16      1.69    [110, 178]
0.221283     7234.068974     0.431399    4   15      1.42    [93, 110]
0.220412     6539.076905     0.117886    4   16      1.60    [114, 191]
0.220412     5844.084837     0.120121    4   17      1.39    [129, 174]
0.220412     5149.092769     0.116841    4   18      1.38    [6, 145]
0.219084     4490.145537     0.115819    4   18      1.41    [6, 169]
0.217758     3806.409006     0.115819    4   17      1.48    [114, 174]
0.216413     3143.206175     0.110169    4   18      1.64    [71, 108]
0.215456     2483.174272     0.129944    4   19      1.60    [47, 55]
0.212977     715.955244      0.436803    4   19      1.67    [99, 126]
0.207519     -2135.647869    0.494497    4   20      1.72    [35, 87]
0.207519     -4987.250981    0.495640    4   21      1.61    [33, 187]
0.207519     -7838.854093    0.499338    4   22      1.71    [151, 172]
0.207519     -10690.457206   0.499330    4   23      1.78    [98, 166]
0.207519     -13542.060318   0.497388    4   24      1.67    [63, 141]
0.205672     -15232.578454   0.370317    4   24      1.73    [53, 144]
0.205034     -17946.432009   0.492242    4   24      1.78    [63, 184]
0.204614     -18581.507173   0.135593    4   24      1.81    [14, 50]
0.203064     -21240.664597   0.496844    4   25      2.11    [2, 3]
0.203064     -23898.340341   0.497175    4   26      1.88    [61, 170]
0.202515     -24465.577161   0.093220    4   27      2.06    [69, 138]
0.199890     -25016.719998   0.091214    4   28      1.91    [167, 175]
0.198656     -27500.912198   0.493877    4   29      1.89    [19, 118]
0.197651     -28063.509315   0.115577    4   29      1.88    [37, 190]
0.196228     -30468.599502   0.487129    4   29      1.99    [8, 35]
0.194294     -32800.033986   0.491525    4   30      1.98    [26, 140]
0.194294     -35131.468469   0.491525    4   31      2.02    [22, 132]
0.194271     -37712.206487   0.491849    4   31      2.02    [2, 89]
0.192967     -38267.959014   0.118239    4   32      2.17    [34, 185]
0.190838     -39243.217562   0.191887    4   31      2.16    [92, 130]
0.189978     -41441.484509   0.488562    4   32      2.26    [9, 152]
0.184701     -42777.758985   0.321892    4   32      2.21    [64, 76]
0.181944     -43231.607598   0.073446    4   33      2.26    [77, 159]
0.181085     -44609.991105   0.328191    4   33      2.34    [59, 155]
0.177306     -46502.271297   0.480177    4   34      2.31    [56, 116]
0.171337     -46906.919167   0.064972    4   35      2.19    [46, 107]
0.170942     -47402.964056   0.091844    4   35      2.38    [142, 190]
0.169425     -48098.865802   0.168820    4   36      2.46    [121, 133]
0.168443     -49842.132885   0.476989    4   36      2.54    [19, 91]
0.167716     -51083.837026   0.281604    4   36      2.36    [28, 144]
0.163545     -51455.436786   0.058302    4   37      2.44    [48, 112]
0.163545     -51827.036547   0.057791    4   38      2.54    [13, 90]
0.163545     -52198.636308   0.059259    4   39      2.59    [39, 100]
0.162786     -52557.461309   0.056301    4   39      2.56    [17, 48]
0.162026     -52914.365426   0.057412    4   38      2.91    [13, 17]
0.158198     -53359.549880   0.102592    4   38      2.63    [51, 60]
0.155102     -53697.875401   0.053161    4   39      2.64    [15, 117]
0.146391     -53993.898442   0.054721    4   38      2.59    [15, 39]
0.145764     -55329.965758   0.432218    4   39      2.68    [1, 11]
0.144708     -55716.898239   0.090395    4   39      2.79    [146, 185]
0.141631     -57256.479042   0.455133    4   38      2.84    [9, 56]
0.141402     -57823.887030   0.144068    4   38      2.82    [52, 133]
0.141348     -59251.928951   0.456547    4   38      2.86    [27, 118]
0.136480     -58758.806460   0.081908    4   38      2.95    [8, 16]
0.134400     -60052.978712   0.449153    4   39      3.10    [62, 78]
0.129317     -61288.053673   0.443808    4   40      3.14    [7, 127]
0.127203     -62509.753765   0.443503    4   41      3.23    [122, 153]
0.124388     -63210.212833   0.200565    4   41      3.24    [10, 179]
0.122074     -63508.059597   0.070880    4   42      3.06    [32, 199]
0.114480     -63834.594691   0.075592    4   42      3.32    [36, 97]
0.111674     -64590.262895   0.432135    6   41      3.24    [3, 16]
0.111060     -65130.427443   0.146893    6   41      4.52    [24, 192]
0.110284     -65982.381434   0.217649    6   41      4.35    [137, 176]
0.108244     -67039.739318   0.430352    6   41      4.48    [33, 148]
0.104807     -66424.411688   0.102098    6   41      4.33    [164, 172]
0.100262     -66779.963252   0.173960    6   41      4.36    [67, 135]
0.099799     -66075.988863   0.104504    7   41      4.68    [35, 57]
0.097743     -66971.612439   0.296623    7   41      6.80    [79, 127]
0.096952     -67992.415492   0.423028    7   41      6.55    [29, 141]
0.095361     -69220.533809   0.418102    7   40      6.58    [98, 187]
0.094023     -70149.337407   0.415254    7   41      6.71    [83, 134]
0.092252     -70368.366086   0.053672    7   41      6.86    [32, 86]
0.092151     -71051.696684   0.176453    7   41      6.85    [160, 181]
0.091448     -70545.168883   0.108966    8   41      8.00    [35, 82]
0.090964     -71449.210560   0.412418    8   42      13.91   [21, 88]
0.090579     -70860.568734   0.110241    11      41      47.82   [89, 172]
0.084000     -71542.741403   0.305085    11      41      246.90      [11, 68]
0.082687     -71892.842992   0.088772    11      40      247.76      [130, 167]
0.082066     -72727.010310   0.403955    11      40      272.42      [21, 43]
0.081564     -73025.273186   0.161017    11      40      267.01      [42, 79]

[TIMER] Compute p: 87.400754
[TIMER] independence_estimate: 38.675459
[TIMER] mtv_query: 1266.062564
[TIMER] Block weight: 986.142300
[TIMER] Cached query: 1271.108807
[TIMER] Find best itemset: 1296.975752
[TIMER] union_of_itemsets: 9.281288
[TIMER] Iterative scaling: 37.317236
[TIMER] Cummulative weight: 148.864291
[TIMER] Singletons of itemsets: 0.000915
[TIMER] Compute blocks: 0.107902
[COUNTER] Independence estimates: 2575136
[COUNTER] Block queries: 20532494
[COUNTER] Total queries: 23107630
[COUNTER] Iterative scaling max iterations: 100
[COUNTER] Independent models: 42