#!/usr/bin/env pypy
#
#   Scratchpad for working with implementation from the root folder.
#

from matplotlib.pylab import plot, ylabel, xlabel, savefig, close, title, figtext
from preprocessing.discretization import *
from preprocessing.preprocessors import remove_empty_samples, compute_relative_values, discrete_dataset_cleaning
import os

from plots.faust_result_discretized import plot_faust_relationships
# plot_faust_relationships()
# run()


# def run_discretization():
#     """
#     TODO: Work in progress. Code to use a phylogenetic tree, and get a
#     daset at a particular depth.
#     """
#     from preprocessing import parser
#     from preprocessing.tree import Tree
#     from utils.dataset_helpers import abundance_matrix
#     from itemsets import binary_vectors_to_ints
#     from utils.files import write_dat_file
#
#     ds = parser.get_dataset()
#     ds = parser.compute_relative_values(ds)
#     t = Tree(ds)
#     bin_ds = t.dataset_at_max_depth(3)
#
#     abundance = abundance_matrix(bin_ds)
#
#     D = binary_vectors_to_ints(abundance)
#
#     write_dat_file('../experiments/1/stool_depth3_discrete.dat', D)
#     headers = []
#     for header in bin_ds[0][2:]:
#         vals = header.split('|')
#         if len(vals) > 1:
#             headers.append('|'.join(vals[-2:]))
#         else:
#             headers.append(vals[0])
#
#     with open('../experiments/1/stool_depth3_discrete.headers', 'wb') as fd:
#         line = ' '.join(headers)
#         fd.write(line)

def write_dataset_to_experiment(file_name, ds):
    from itemsets import binary_vectors_to_ints
    from utils.files import write_dat_file
    import pickle
    import itemsets
    # Write .dat file
    abundance = abundance_matrix(ds)
    D = binary_vectors_to_ints(abundance)
    write_dat_file(file_name + '.dat', D)

    # Create a header file
    headers = []
    for header in ds[0][2:]:
        vals = header.split('|')
        if len(vals) > 1:
            headers.append('|'.join(vals[-2:]))
        else:
            headers.append(vals[0])

    with open(file_name + '.headers', 'wb') as fd:
        line = ' '.join(headers)
        fd.write(line)

    # save the raw dataset
    with open(file_name + '.pickle', 'wb') as fd:
        pickle.dump(ds, fd)


def run_discretization_all_nodes():
    """
    TODO: Work in progress. Code to use a phylogenetic tree, and get a
    daset for the entire phylogenetic tree
    """
    from preprocessing import parser
    from preprocessing.tree import Tree
    from utils.dataset_helpers import abundance_matrix

    # Get the stool dataset and discretize it
    ds = parser.get_dataset()
    ds = compute_relative_values(ds)
    t = Tree(ds)
    print 'tree nodes before: ', t.count_nodes()
    print 'tree leafs before: ', t.count_leafs()
    ds = t.dataset_for_all_nodes()
    ds = median_discretization(ds)
    ds = discrete_dataset_cleaning(ds, 0.05)

    print 'Final number of attributes: ', len(ds[0]) - 2

    write_dataset_to_experiment('../experiments/1/Stool_maxent_discretized_all_nodes', ds)


# run_discretization_all_nodes()


def run_discretization_faust_nodes_and_leafs():
    """
    TODO: This currently result in only 37 attributes, and 32 after cleaning..
    Is this enough? Can we search the tree differently?
    """
    from preprocessing import parser
    from preprocessing.tree import Tree
    from utils.dataset_helpers import abundance_matrix
    from itemsets import binary_vectors_to_ints
    from utils.files import write_dat_file
    from preprocessing import faust_parser
    import itemsets

    # Get the Faust result clade names
    faust_results = faust_parser.results()
    faust_clades = []
    for faust_result in faust_results:
        faust_clades.append(faust_result.clade_1)
        faust_clades.append(faust_result.clade_2)

    # Get the stool dataset and discretize it
    ds = parser.get_dataset()
    ds = compute_relative_values(ds)
    t = Tree(ds)

    ds = t.dataset_for_clades_or_leaf(faust_clades)
    print 'Attributes: ', len(ds[0][2:])
    ds = median_discretization(ds)
    ds = discrete_dataset_cleaning(ds)
    print 'Attributes after cleaning: ', len(ds[0][2:])

    write_dataset_to_experiment('../experiments/5/Stool_maxent_discretized_faust_nodes_and_leafs', ds)

# run_discretization_faust_nodes_and_leafs()

def run_discretization_for_tree_depth(depth):
    """
    Experiment with all nodes at a given depth

    depth 6:
    Cleaning:
    Attributes:  166
    discrete dataset cleaning, removed bacteria:  65
    Attributes after cleaning:  101

    depth 5:
    Attributes:  66
    discrete dataset cleaning, removed bacteria:  21
    Attributes after cleaning:  45
    """
    from preprocessing import parser
    from preprocessing.tree import Tree
    from preprocessing import faust_parser
    import itemsets

    # Get the stool dataset and discretize it
    ds = parser.get_dataset()
    ds = compute_relative_values(ds)
    t = Tree(ds)
    ds = t.dataset_at_depth(depth)

    print 'Attributes: ', len(ds[0][2:])
    ds = median_discretization(ds)
    ds = discrete_dataset_cleaning(ds, 0.20)
    print 'Attributes after cleaning: ', len(ds[0][2:])

    write_dataset_to_experiment('../experiments/4/Stool_maxent_discretized_nodes_depth_6_020', ds)


# run_discretization_for_tree_depth(6)

def load_model():
    from mtv import MTV
    from utils import files
    import itemsets
    headers = files.parse_header_file('../experiments/1/Stool_maxent_discretized_all_nodes.headers')
    C = files.parse_dat_file('../experiments/1/summary.dat')
    D = files.parse_dat_file('../experiments/1/Stool_maxent_discretized_all_nodes.dat')
    # print clade names
    for X in C:
        print itemsets.to_index_list(X, headers)



def plot_BIC_score(BIC_SCORE, path):
    xlabel('|C|')
    ylabel('BIC score')
    plot(BIC_SCORE)
    savefig(os.path.join(path, 'BIC.png'))
    close()

def plot_heuristic(heuristic, path):
    xlabel('|C|')
    ylabel('h')
    plot(heuristic)
    savefig(os.path.join(path, 'heuristic.png'))
    close()

def plot_independent_models(independent_models, path):
    xlabel('|C|')
    ylabel('Independent models')
    plot(independent_models)
    savefig(os.path.join(path, 'independent_models.png'))
    close()

def plot_running_time(running_time, path):
    xlabel('|C|')
    ylabel('MTV iteration in secs.')
    plot([x for x in range(len(running_time))], running_time)
    savefig(os.path.join(path, 'running_time.png'))
    close()

def plot_size_of_c(size_of_c, path):
    xlabel('MTV iteration')
    ylabel('Max model size |Ci|')
    plot([x for x in range(len(size_of_c))], size_of_c)
    savefig(os.path.join(path, 'size_of_c.png'))
    close()



def build_summary_table():
    # Construct summary table
    pass


def compare_to_faust():
    """
    Go through the faust results and check if our pairs occur
    :return:
    """
    from preprocessing.faust_parser import results
    from utils.files import parse_header_file, parse_dat_file
    from itemsets import to_index_list
    from itertools import combinations
    from preprocessing import parser
    from preprocessing.tree import Tree
    from preprocessing import faust_parser
    import itemsets

    # Get the stool dataset, and construct the
    # phylogenetic tree, so we can look up
    # ancestors of the patterns we have discovered
    ds = parser.get_dataset()
    tree = Tree(ds)

    headers = parse_header_file('../experiments/4/Stool_maxent_discretized_nodes_depth_6_020.headers')
    summary = parse_dat_file('../experiments/4/summary.dat')
    # Get the indeces of the pair
    bin_indeces = [to_index_list(x) for x in summary]

    # Get summary itemsets by their clade names
    patterns = []
    for indeces in bin_indeces:
        pattern = []
        for index in indeces:
            # co-occurrence
            if index > len(headers):
                index = index - len(headers)
            pattern.append(headers[index])
        patterns.append(pattern)

    faust_results = results()
    genues_in_faust = []
    for faust_result in faust_results:
        a = faust_result.clade_1
        b = faust_result.clade_2
        if a in tree.nodes and b in tree.nodes:
            node_a = tree.nodes[a]
            node_b = tree.nodes[b]
            if node_a.depth == 6 and node_b.depth == 6:
                genues_in_faust.append((a,b))
    print 'genus in faust: ', len(genues_in_faust)

    # Check every pair in every pattern for existence in the faust results
    print 'In faust:'
    for pattern in patterns:
        for a, b in combinations(pattern, 2):

            # Get nodes for our pattern
            node_a = tree.nodes[a]
            node_b = tree.nodes[b]
            # print 'depth a: ', node_a.depth
            # print 'depth b: ', node_b.depth

            for faust_result in faust_results:
                if faust_result.clade_1 == a or faust_result.clade_2 == a:
                    if faust_result.clade_1 == b or faust_result.clade_2 == b:
                        print 'Genus results:'
                        print 'Faust: %s %s, %d' % (faust_result.clade_1, faust_result.clade_2, faust_result.direction)
                        print '%s, %s' % (a.replace('|', '-'), b.replace('|', '-'))

                        if (faust_result.clade_1, faust_result.clade_2) in genues_in_faust:
                            genues_in_faust.remove((faust_result.clade_1, faust_result.clade_2))
                    elif faust_result.clade_1 in tree.nodes and faust_result.clade_2 in tree.nodes:
                        faust_a = tree.nodes[faust_result.clade_1]
                        faust_b = tree.nodes[faust_result.clade_2]

                        # Do not look for stuff that is too general
                        # only parent nodes
                        parent_depth = 3
                        if faust_a.depth <= parent_depth or faust_b.depth <= parent_depth:
                            continue

                        # Node a
                        is_descendents = 0
                        res = ''
                        if node_a.is_in_lineage(faust_a)  and node_b.is_in_lineage(faust_b):
                            res += 'a in a, b in b'
                            is_descendents = True
                        if node_a.is_in_lineage(faust_b)  and node_b.is_in_lineage(faust_a):
                            res += 'a in b, b in a'
                            is_descendents = True

                        if is_descendents:
                            print '####'
                            print 'Result in same lineage: ' + res
                            print '%s, %s' % (a, b)
                            print 'Faust %d' % faust_result.direction
                            print '%s, %s' % (faust_a.name, faust_b.name)
                            print '####'





    print 'Not found at genus level: ', genues_in_faust
# compare_to_faust()



def clade_table():
    from utils.files import parse_header_file, parse_dat_file
    from itemsets import to_index_list
    headers = parse_header_file('../experiments/4/Stool_maxent_discretized_nodes_depth_6_020.headers')

    summary = parse_dat_file('../experiments/4/summary.dat')
    # Get the indeces of the pair
    bin_indeces = [to_index_list(x) for x in summary]


    clades = []
    for indeces in bin_indeces:
        pattern = []
        for index in indeces:
            # co-occurrence
            if index > len(headers):
                index = index - len(headers)

            pattern.append(headers[index])

        clades.append(pattern)
        # print '[' + ', '.join(pattern) + ']'
        print '\item {\small '
        for clade in pattern:
            line = '%s, ' % clade.replace('|', '-')
            if clade == pattern[-1]:
                line = line.replace(',', '')
            line = line.replace('_', '\\_')
            print line
        print '}'
        print ''
    print 'Clades in itemset: '

    # for clade1, clade2 in clades:
    #     print '%s & %s\\\\' % (clade1, clade2)

# clade_table()

def clade_pair_abundances():
    from utils.files import parse_header_file, parse_dat_file
    from itemsets import to_index_list
    from plots.clade_correlation import plot_clades_relationships
    from itertools import combinations
    headers = parse_header_file('../experiments/1/Stool_maxent_discretized_all_nodes.headers')
    headers = headers + headers

    # parse_dat_file returns a list of ints
    summary = parse_dat_file('../experiments/tmp/summary.dat')
    # Get the indeces of the pair
    bin_indeces = [to_index_list(x) for x in summary]


    clades = []
    for pattern in bin_indeces:
        for binindex1, binindex2 in combinations(pattern, 2):
            clade1 = headers[binindex1]
            clade2 = headers[binindex2]
            clades.append((clade1, clade2))

    plot_clades_relationships(clades, '../experiments/1/plots/')

# clade_pair_abundances()

def plot_clades():
    from plots.clade_correlation import plot_clades_relationships

    # Plot all combs
    # lh = ['Ruminococcaceae|Oscillibacter', 'Ruminococcaceae|Anaerotruncus', 'Ruminococcaceae|unclassified', 'Ruminococcaceae|Ruminococcus', 'Ruminococcaceae|Subdoligranulum', 'Incertae_Sedis_XIII|Anaerovorax', 'Coriobacteriaceae|Collinsella']
    # clades = []
    # for c in lh:
    #     clades.append((c, 'Bacteroidaceae|Bacteroides'))

    clades = [('Ruminococcaceae|unclassified', 'Bacteroidaceae|Bacteroides'),
              ('Ruminococcaceae|unclassified', 'Bacteroidia|Bacteroidales'),
              ('Ruminococcaceae|unclassified', 'Bacteroidales|Prevotellaceae'),
              ('Ruminococcaceae|unclassified', 'Bacteroidales|Porphyromonadaceae'),
              ('Ruminococcaceae|unclassified', 'Bacteroidales|Rikenellaceae'),
              ('Ruminococcaceae|unclassified', 'Bacteroidales|unclassified'),
              ('Ruminococcaceae|unclassified', 'Ruminococcaceae|Anaerofilum'),
              ('Ruminococcaceae|unclassified', 'Rikenellaceae|Alistipes')]
    # clades = [['Ruminococcaceae|unclassified', 'Bacteroidaceae|Bacteroides']]
    # clades = [('Bacteroidaceae|Bacteroides', 'Prevotellaceae|unclassified')]

    plot_clades_relationships(clades, '../experiments/4/plots/')

# plot_clades()

def read_run_results(run_results_file):
    heuristics = []
    BIC_scores = []
    independent_models = []
    size_of_c = []
    iteration_time = []
    relation_ships = []
    queries = []
    with open(run_results_file) as fd:
        for line in fd:
            if '\n' in line:
                line = line.replace('\n', '')
            chunks = line.split(' ')
            chunks = [c for c in chunks if c != '' and not ('\t' in c)]
            heuristics.append(float(chunks[0]))
            BIC_scores.append(float(chunks[1]))
            queries.append(float(chunks[2]))
            size_of_c.append(int(chunks[3]))
            independent_models.append(int(chunks[4]))
            iteration_time.append(float(chunks[5]))
            relation_ships.append(chunks[6])

    return heuristics, BIC_scores, independent_models, size_of_c, iteration_time, relation_ships, queries

# plot_clades()

# from preprocessing import faust_parser
# res = faust_parser.results()
# for r in res:
#     print r.clade_1 + ' + ' + r.clade_1

def plot_run_results(run_result_folder):
    path = os.path.join(run_result_folder, 'run_result.txt')
    heuristics, BIC_scores, independent_models, size_of_c, iteration_time, relation_ships, queries = read_run_results(path)

    plot_BIC_score(BIC_scores, run_result_folder)
    plot_heuristic(heuristics, run_result_folder)
    plot_independent_models(independent_models, run_result_folder)
    plot_size_of_c(size_of_c, run_result_folder)
    plot_running_time(iteration_time, run_result_folder)

# plot_run_results('../experiments/1/')

def format_stats(summary_file):
    """
    Reads a file containing a copy of the MTV output
    :param f:
    """

    heuristics, BIC_scores, independent_models, size_of_c, iteration_time, relation_ships, queries = read_run_results(summary_file)

    print 'heuristics =', heuristics
    print 'BIC_scores =', BIC_scores
    print 'independent_models =', independent_models
    print 'size_of_c =', size_of_c
    print 'iteration_time =', iteration_time
    print 'relation_ships: ', relation_ships
    print
    # for latex table
    print 'LATEX:'
    for index, i in enumerate(heuristics):
        line = '$ %d $ & ' % (index + 1)
        line += '$ %s $ & ' % relation_ships[index]
        line += '$ %.3f $ & ' % queries[index]
        line += '$ %d $ & ' % independent_models[index]
        line += '$ %d $ & ' % size_of_c[index]
        line += '$ %.1f $ &' % iteration_time[index]
        line += '$ %.3f $ & ' % heuristics[index]
        line += '$ %d $ ' % BIC_scores[index]
        print line + '\\\\'

# format_stats('../experiments/4/run_result.txt')

def write_tree():
    from preprocessing.tree import Tree
    from preprocessing.parser import get_dataset
    ds=get_dataset()
    t = Tree(ds)
    xml=t.root.to_xml()
    with open('tree.xml', 'wb') as fd:
       fd.write(xml)

# write_tree()

# from preprocessing.tree import Tree
#
# from preprocessing import parser
#
# ds = parser.get_dataset()
#
# t = Tree(ds)
# clades = ['Bacteroidaceae|Bacteroides', 'Bacteroidia|Bacteroidales',
#           'Bacteroidales|Prevotellaceae', 'Bacteroidales|Porphyromonadaceae',
#           'Bacteroidales|Rikenellaceae', 'Bacteroidales|unclassified',
#             'Ruminococcaceae|unclassified', 'Ruminococcaceae|Anaerofilum']
#
# s = t.dot_graph_for_clades(clades)
# print s
