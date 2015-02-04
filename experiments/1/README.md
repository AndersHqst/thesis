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


    Model predictions:
query [70, 125] with fr 0.251412 query 0.247602
query [125, 126] with fr 0.251412 query 0.249664
query [29, 72] with fr 0.197740 query 0.197740
query [11, 108] with fr 0.192090 query 0.192084
query [65, 170] with fr 0.223164 query 0.223233
query [2, 190] with fr 0.194915 query 0.194915
query [85, 97] with fr 0.364407 query 0.366753
query [85, 104] with fr 0.364407 query 0.364407
query [127, 186] with fr 0.158192 query 0.158155
query [103, 149] with fr 0.155367 query 0.152935
query [12, 195] with fr 0.152542 query 0.152542
query [39, 128] with fr 0.152542 query 0.151698
query [19, 124] with fr 0.389831 query 0.384050
query [12, 177] with fr 0.152542 query 0.153815
query [24, 141] with fr 0.403955 query 0.403482
query [98, 147] with fr 0.409605 query 0.406639
query [39, 195] with fr 0.152542 query 0.155108
query [87, 163] with fr 0.138418 query 0.135999
query [6, 8] with fr 0.285311 query 0.285329
query [22, 90] with fr 0.440678 query 0.430739
query [101, 107] with fr 0.440678 query 0.438368
query [22, 101] with fr 0.440678 query 0.434957
query [9, 71] with fr 0.115819 query 0.117678
query [31, 55] with fr 0.115819 query 0.115819
query [26, 86] with fr 0.115819 query 0.115819
query [31, 194] with fr 0.115819 query 0.117874
query [9, 26] with fr 0.115819 query 0.119680
query [74, 107] with fr 0.440678 query 0.440155
query [92, 129] with fr 0.110169 query 0.110169
query [145, 153] with fr 0.129944 query 0.129944
query [28, 49] with fr 0.500000 query 0.494623
query [113, 165] with fr 0.500000 query 0.498246
query [59, 137] with fr 0.500000 query 0.503168
query [34, 102] with fr 0.500000 query 0.499092
query [13, 167] with fr 0.500000 query 0.495628
query [56, 98] with fr 0.372881 query 0.366984
query [16, 59] with fr 0.500000 query 0.500180
query [127, 150] with fr 0.135593 query 0.135593
query [197, 198] with fr 0.497175 query 0.501405
query [30, 139] with fr 0.497175 query 0.497175
query [62, 131] with fr 0.093220 query 0.093220
query [25, 33] with fr 0.090395 query 0.088043
query [82, 181] with fr 0.494350 query 0.497685
query [10, 87] with fr 0.118644 query 0.118643
query [113, 192] with fr 0.494350 query 0.489026
query [60, 174] with fr 0.491525 query 0.491525
query [68, 178] with fr 0.491525 query 0.491525
query [15, 166] with fr 0.118644 query 0.118292
query [111, 197] with fr 0.491525 query 0.503208
query [48, 191] with fr 0.488701 query 0.490069
query [70, 108] with fr 0.194915 query 0.196894
query [19, 136] with fr 0.319209 query 0.317208
query [41, 123] with fr 0.073446 query 0.073446
query [24, 45] with fr 0.330508 query 0.329410
query [84, 144] with fr 0.480226 query 0.481159
query [10, 58] with fr 0.093220 query 0.094115
query [93, 154] with fr 0.064972 query 0.064972
query [56, 172] with fr 0.279661 query 0.278442
query [67, 79] with fr 0.169492 query 0.169494
query [109, 181] with fr 0.474576 query 0.476021
query [183, 187] with fr 0.059322 query 0.059168
query [100, 161] with fr 0.059322 query 0.057912
query [88, 110] with fr 0.059322 query 0.057769
query [152, 183] with fr 0.059322 query 0.058224
query [88, 152] with fr 0.059322 query 0.058696
query [103, 140] with fr 0.104520 query 0.105412
query [83, 185] with fr 0.053672 query 0.053192
query [83, 100] with fr 0.053672 query 0.054664
query [189, 199] with fr 0.432203 query 0.432185
query [15, 54] with fr 0.090395 query 0.090395
query [67, 148] with fr 0.144068 query 0.144068
query [144, 191] with fr 0.454802 query 0.455681
query [82, 173] with fr 0.454802 query 0.457477
query [165, 184] with fr 0.084746 query 0.084092
query [122, 138] with fr 0.449153 query 0.449153
query [73, 193] with fr 0.443503 query 0.443788
query [47, 78] with fr 0.443503 query 0.443503
query [21, 190] with fr 0.200565 query 0.202919
query [1, 168] with fr 0.070621 query 0.070878
query [103, 164] with fr 0.076271 query 0.075618
query [184, 197] with fr 0.432203 query 0.448467
query [63, 141] with fr 0.217514 query 0.215397
query [8, 176] with fr 0.146893 query 0.146893
query [13, 52] with fr 0.429379 query 0.428008
query [36, 49] with fr 0.101695 query 0.102738
query [143, 165] with fr 0.104520 query 0.102899
query [65, 133] with fr 0.172316 query 0.172316
query [16, 171] with fr 0.420904 query 0.427723
query [73, 121] with fr 0.296610 query 0.296610
query [34, 167] with fr 0.418079 query 0.415759
query [66, 117] with fr 0.415254 query 0.415247
query [114, 168] with fr 0.053672 query 0.053672
query [19, 40] with fr 0.175141 query 0.176300
query [113, 118] with fr 0.110169 query 0.109361
query [112, 179] with fr 0.412429 query 0.412419
query [28, 111] with fr 0.110169 query 0.110734
query [113, 116] with fr 0.115819 query 0.113930
query [25, 125] with fr 0.090395 query 0.090855
query [113, 115] with fr 0.115819 query 0.113950
query [132, 189] with fr 0.305085 query 0.305085
query [157, 179] with fr 0.403955 query 0.403955

k=100, m=2, s=0.050000

MTV run time:  4133.04253411

Summary: 
Heuristic    BIC score   p       Itemsets
x.xxxxxx     40518.023230    (No query)      I+seed
0.258570     39074.001363    0.247602    [70, 125]
0.256374     37672.768919    0.249664    [125, 126]
0.253540     36523.551047    0.197740    [29, 72]
0.249014     35420.522715    0.192084    [11, 108]
0.247358     34257.680567    0.223233    [65, 170]
0.246283     33213.776123    0.194915    [2, 190]
0.245794     31143.191777    0.366753    [85, 97]
0.243293     29203.731224    0.364407    [85, 104]
0.242473     28179.520529    0.158155    [127, 186]
0.241374     27357.136266    0.152935    [103, 149]
0.240228     26457.314743    0.152542    [12, 195]
0.240228     25557.493220    0.151698    [39, 128]
0.240036     23344.647343    0.384050    [19, 124]
0.238602     22498.867796    0.153815    [12, 177]
0.236503     20167.517834    0.403482    [24, 141]
0.235029     17880.834902    0.406639    [98, 147]
0.235404     17037.223841    0.155108    [39, 195]
0.233750     16112.973721    0.135999    [87, 163]
0.233325     14850.238088    0.285329    [6, 8]
0.226349     12346.868610    0.430739    [22, 90]
0.226349     9843.499133     0.438368    [101, 107]
0.221283     7208.363911     0.434957    [22, 101]
0.220412     6820.039491     0.117678    [9, 71]
0.220412     5818.379774     0.115819    [31, 55]
0.220412     5123.387706     0.115819    [26, 86]
0.219084     4448.255094     0.117874    [31, 194]
0.217758     3772.836715     0.119680    [9, 26]
0.217083     2059.473120     0.440155    [74, 107]
0.216413     1091.493171     0.110169    [92, 129]
0.215456     729.578970      0.129944    [145, 153]
0.207519     -2122.024143    0.494623    [28, 49]
0.207519     -4973.627255    0.498246    [113, 165]
0.207519     -7825.230367    0.503168    [59, 137]
0.207519     -10676.833480   0.499092    [34, 102]
0.207519     -13528.436592   0.495628    [13, 167]
0.205672     -15219.872124   0.366984    [56, 98]
0.205034     -17962.456052   0.500180    [16, 59]
0.204614     -18593.613403   0.135593    [127, 150]
0.203064     -21282.938091   0.501405    [197, 198]
0.203064     -23914.643591   0.497175    [30, 139]
0.202515     -24481.880411   0.093220    [62, 131]
0.199890     -25033.023249   0.088043    [25, 33]
0.198656     -27517.215448   0.497685    [82, 181]
0.197651     -28083.386176   0.118643    [10, 87]
0.196228     -30776.483188   0.489026    [113, 192]
0.194294     -32918.499379   0.491525    [60, 174]
0.194294     -35438.983164   0.491525    [68, 178]
0.192967     -35995.344703   0.118292    [15, 166]
0.192951     -38268.891606   0.503208    [111, 197]
0.189978     -40791.954931   0.490069    [48, 191]
0.189960     -41267.574051   0.196894    [70, 108]
0.184701     -42848.591089   0.317208    [19, 136]
0.181944     -43126.879874   0.073446    [41, 123]
0.181085     -44426.150664   0.329410    [24, 45]
0.177306     -46378.204154   0.481159    [84, 144]
0.172150     -46756.464839   0.094115    [10, 58]
0.171337     -47287.659340   0.064972    [93, 154]
0.169732     -48508.602165   0.278442    [56, 172]
0.169425     -49019.870757   0.169494    [67, 79]
0.167229     -50900.802236   0.476021    [109, 181]
0.163545     -51371.186968   0.059168    [183, 187]
0.163545     -51644.872583   0.057912    [100, 161]
0.163545     -52016.472344   0.057769    [88, 110]
0.162786     -52375.297345   0.058224    [152, 183]
0.162026     -52703.087054   0.058696    [88, 152]
0.158198     -53135.426473   0.105412    [103, 140]
0.155102     -53509.030961   0.053192    [83, 185]
0.146391     -53784.329378   0.054664    [83, 100]
0.145764     -55103.208592   0.432185    [189, 199]
0.145540     -55522.027105   0.090395    [15, 54]
0.142248     -56100.451658   0.144068    [67, 148]
0.141160     -57595.163520   0.455681    [144, 191]
0.140678     -59291.384504   0.457477    [82, 173]
0.136126     -58272.971606   0.084092    [165, 184]
0.134400     -59771.526769   0.449153    [122, 138]
0.129317     -60926.457611   0.443788    [73, 193]
0.127203     -62148.157703   0.443503    [47, 78]
0.124020     -62917.165085   0.202919    [21, 190]
0.122074     -63161.589680   0.070878    [1, 168]
0.114224     -63560.434913   0.075618    [103, 164]
0.110440     -64608.927869   0.448467    [184, 197]
0.110284     -65661.690073   0.215397    [63, 141]
0.109967     -65947.965534   0.146893    [8, 176]
0.108244     -67034.089048   0.428008    [13, 52]
0.104807     -66490.520913   0.102738    [36, 49]
0.101086     -66146.382930   0.102899    [143, 165]
0.100262     -66643.274880   0.172316    [65, 133]
0.098557     -67781.352497   0.427723    [16, 171]
0.097757     -68627.903569   0.296610    [73, 121]
0.095361     -69743.988873   0.415759    [34, 167]
0.094023     -70922.235057   0.415247    [66, 117]
0.092252     -70889.076993   0.053672    [114, 168]
0.091989     -71657.312104   0.176300    [19, 40]
0.091712     -70619.837564   0.109361    [113, 118]
0.090964     -71712.086472   0.412419    [112, 179]
0.091136     -71094.303759   0.110734    [28, 111]
0.086656     -70800.891468   0.113930    [113, 116]
0.085914     -71102.443440   0.090855    [25, 125]
0.084254     -69939.285118   0.113950    [113, 115]
0.084000     -71120.488168   0.305085    [132, 189]
0.082054     -71562.434786   0.403955    [157, 179]

[TIMER] Compute p: 164.575778
[TIMER] Find best itemset: 2885.087576
[TIMER] Block weight: 3529.845153
[TIMER] Iterative scaling: 1245.407990
[TIMER] Cummulative weight: 317.205300
[TIMER] Singletons of itemsets: 4.145017
[TIMER] Compute blocks: 1.434563
[COUNTER] Independence estimates: 3784525
[COUNTER] Block queries: 23946104
[COUNTER] Total queries: 27730629
[COUNTER] Iterative scaling max iterations: 100
[COUNTER] Independent models: 42