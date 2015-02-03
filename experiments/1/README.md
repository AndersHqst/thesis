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
    Create scatter plots for summary, with discretization lines.
        Put representative plot



1 attempt:
./main.py -f ../experiments/1/Stool_maxent_discretized_all_nodes.dat -m 2 -k 20 -o ../experiments/1/summary.dat --debug
notes:
    with -k 1 -m2 running time is ~7 secs. These looks almost linear in k, ie 7*k for some small k
    with -k1 -m 3 running time is took several minutes with no results

output:
Model predictions:
query [137, 170] with fr 0.364407 query 0.364326
query [158, 170] with fr 0.364407 query 0.364407
query [10, 12] with fr 0.285311 query 0.285311
query [36, 147] with fr 0.440678 query 0.435894
query [164, 174] with fr 0.440678 query 0.430836
query [36, 164] with fr 0.440678 query 0.440517
query [95, 159] with fr 0.372881 query 0.372937
query [49, 85] with fr 0.500000 query 0.500000
query [102, 270] with fr 0.500000 query 0.500000
query [84, 298] with fr 0.500000 query 0.500000
query [95, 267] with fr 0.279661 query 0.279661
query [51, 214] with fr 0.500000 query 0.500000
query [294, 311] with fr 0.457627 query 0.456354
query [179, 277] with fr 0.412429 query 0.412331
query [207, 294] with fr 0.333333 query 0.333333
query [115, 131] with fr 0.500000 query 0.501347
query [115, 276] with fr 0.500000 query 0.500000
query [246, 277] with fr 0.403955 query 0.403955
query [192, 304] with fr 0.274011 query 0.274011
query [131, 279] with fr 0.392655 query 0.395717

k=20, m=2, s=0.250000

MTV run time:  419.429175138

Summary: 
Heuristic    BIC score   p       Itemsets
x.xxxxxx     519874.594296   (No query)      I+seed
0.245794     517962.693856   0.364326    [137, 170]
0.243293     516061.213482   0.364407    [158, 170]
0.233325     514813.277966   0.285311    [10, 12]
0.226349     512648.882621   0.435894    [36, 147]
0.226349     510348.065932   0.430836    [164, 174]
0.221283     508099.807785   0.440517    [36, 164]
0.207940     506675.996693   0.372937    [95, 159]
0.207519     503947.167701   0.500000    [49, 85]
0.189113     501725.365735   0.500000    [102, 270]
0.186581     499534.306747   0.500000    [84, 298]
0.169758     498531.911082   0.279661    [95, 267]
0.155751     496569.229190   0.500000    [51, 214]
0.140221     494934.507771   0.456354    [294, 311]
0.090964     494210.409506   0.412331    [179, 277]
0.090546     493188.273285   0.333333    [207, 294]
0.083442     491577.573537   0.501347    [115, 131]
0.083432     489971.759044   0.500000    [115, 276]
0.081889     489298.890289   0.403955    [246, 277]
0.072630     488840.644309   0.274011    [192, 304]
0.069451     488246.597245   0.395717    [131, 279]

[TIMER] Compute p: 71.990916
[TIMER] Find best itemset: 376.228015
[TIMER] Block weight: 27.879019
[TIMER] Cached query: 361.312640
[TIMER] Iterative scaling: 43.063557
[TIMER] Cummulative weight: 238.999193
[TIMER] Compute blocks: 0.024567
[COUNTER] Independence estimates: 1434600
[COUNTER] Block queries: 1313264
[COUNTER] Total queries: 2747864
[COUNTER] Iterative scaling max iterations: 100
[COUNTER] Independent models: 12

x.xxxxxx     519874.594296   (No query)      I+seed
heurestics = [0.245794,
0.243293,
0.233325,
0.226349,
0.226349,
0.221283,
0.207940,
0.207519,
0.189113,
0.186581,
0.169758,
0.155751,
0.140221,
0.090964,
0.090546,
0.083442,
0.083432,
0.081889,
0.072630,
0.069451]

BIC_SCORE = [517962.693856,
516061.213482,
514813.277966,
512648.882621,
510348.065932,
508099.807785,
506675.996693,
503947.167701,
501725.365735,
499534.306747,
498531.911082,
496569.229190,
494934.507771,
494210.409506,
493188.273285,
491577.573537,
489971.759044,
489298.890289,
488840.644309,
488246.597245]

# Sumamry converted with headers:
['Burkholderiales|Alcaligenaceae', 'Synergistetes|Synergistia']
['Flavobacteriales|unclassified', 'Synergistetes|Synergistia']
['Veillonellaceae|Megamonas', 'Bacteria|Bacteroidetes']
['Porphyromonadaceae|unclassified', 'Actinobacteria|Actinobacteria']
['Actinomycetales|Corynebacteriaceae', 'Aeromonadales|Succinivibrionaceae']
['Porphyromonadaceae|unclassified', 'Actinomycetales|Corynebacteriaceae']
['Ruminococcaceae|Subdoligranulum', 'Ruminococcaceae|Ethanoligenens']
['Erysipelotrichaceae|Coprobacillus', 'Peptococcaceae|Peptococcus']
['Enterobacteriaceae|Escherichia/Shigella', 'Proteobacteria|Epsilonproteobacteria']
['Alphaproteobacteria|Sphingomonadales', 'Bacteria|Cyanobacteria']
['Ruminococcaceae|Subdoligranulum', 'Neisseriaceae|unclassified']
['Veillonellaceae|Acidaminococcus', 'Pasteurellaceae|Aggregatibacter']
['Victivallaceae|Victivallis', 'Coriobacteriaceae|unclassified']
['Proteobacteria|Betaproteobacteria', 'Verrucomicrobiaceae|Akkermansia']
['Anaeroplasmataceae|Asteroleplasma', 'Victivallaceae|Victivallis']
['Fusobacteria|Fusobacteria', 'Firmicutes|unclassified']
['Fusobacteria|Fusobacteria', 'Porphyromonadaceae|Dysgonomonas']
['Coriobacteriaceae|Enterorhabdus', 'Verrucomicrobiaceae|Akkermansia']
['Campylobacterales|Campylobacteraceae', 'Bacteria']
['Firmicutes|unclassified', 'Actinobacteria|Actinomycetales']
