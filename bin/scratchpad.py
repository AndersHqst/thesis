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
    ds = discrete_dataset_cleaning(ds)

    t2 = Tree(ds)
    print 'number of attributes: ', len(ds[0]) - 2
    print 'tree nodes after: ', t2.count_nodes()
    print 'tree leafs after: ', t2.count_leafs()

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
    ds = discrete_dataset_cleaning(ds, 0.45)
    print 'Attributes after cleaning: ', len(ds[0][2:])

    write_dataset_to_experiment('../experiments/4/Stool_maxent_discretized_nodes_depth_6_045', ds)


run_discretization_for_tree_depth(6)

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
    savefig(path)

def plot_heuristic(heuristic, path):
    xlabel('|C|')
    ylabel('h')
    plot(heuristic)
    savefig(path)

def plot_independent_models(independent_models, path):
    xlabel('|C|')
    ylabel('Independent models')
    plot(independent_models)
    savefig(path)

def plot_running_time(running_time, offset, path):
    xlabel('|C|')
    ylabel('MTV iteration in secs.')
    plot([x+offset for x in range(len(running_time[offset:]))], running_time[offset:])
    savefig(path)



def build_summary_table():
    # Construct summary table
    pass




def clade_table():
    from utils.files import parse_header_file, parse_dat_file
    from itemsets import to_index_list
    headers = parse_header_file('../experiments/4/Stool_maxent_discretized_nodes_depth_6.headers')

    summary = parse_dat_file('../experiments/4/summary.dat')
    # Get the indeces of the pair
    bin_indeces = [to_index_list(x) for x in summary[:10]]

    bin_indeces = [[33, 10], [33, 11]]

    clades = []
    for indeces in bin_indeces:
        name = []
        for index in indeces:
            name.append(headers[index])

        clades.append(name)
        print '[' + ', '.join(name) + ']'

    print 'Clades in itemset: '

    # for clade1, clade2 in clades:
    #     print '%s & %s\\\\' % (clade1, clade2)

# clade_table()

def clade_pair_abundances():
    from utils.files import parse_header_file, parse_dat_file
    from itemsets import to_index_list
    from plots.clade_correlation import plot_clades_relationships
    headers = parse_header_file('../experiments/1/Stool_maxent_discretized_all_nodes.headers')

    # parse_dat_file returns a list of ints
    summary = parse_dat_file('../experiments/1/summary.dat')
    # Get the indeces of the pair
    bin_indeces = [to_index_list(x) for x in summary[:50]]

    clades = []
    for binindex1, binindex2 in bin_indeces:
        clade1 = headers[binindex1]
        clade2 = headers[binindex2]
        clades.append((clade1, clade2))

    plot_clades_relationships(clades, '../experiments/1/plots_top_10/')

# clade_pair_abundances()

def plot_clades():
    from plots.clade_correlation import plot_clades_relationships
    #[Ruminococcaceae|Oscillibacter, Ruminococcaceae|unclassified, Ruminococcaceae|Ruminococcus, Ruminococcaceae|Subdoligranulum, Ruminococcaceae|Sporobacter, Incertae_Sedis_XIII|Anaerovorax]
    # clades = [('Incertae_Sedis_XIII|Anaerovorax', 'Ruminococcaceae|Oscillibacter'),
    #     ('Incertae_Sedis_XIII|Anaerovorax', 'Ruminococcaceae|unclassified'),
    #     ('Incertae_Sedis_XIII|Anaerovorax', 'Ruminococcaceae|Ruminococcus'),
    #     ('Incertae_Sedis_XIII|Anaerovorax', 'Ruminococcaceae|Subdoligranulum'),
    #     ('Incertae_Sedis_XIII|Anaerovorax', 'Ruminococcaceae|Sporobacter')]

    # clades = [('Ruminococcaceae|Sporobacter', 'Ruminococcaceae|Oscillibacter'),
    #     ('Ruminococcaceae|Sporobacter', 'Ruminococcaceae|unclassified'),
    #     ('Ruminococcaceae|Sporobacter', 'Ruminococcaceae|Ruminococcus'),
    #     ('Ruminococcaceae|Sporobacter', 'Ruminococcaceae|Subdoligranulum')]

    # clades = [('Veillonellaceae|unclassified', 'Lachnospiraceae|unclassified'),
    #           ('Veillonellaceae|unclassified', 'Lachnospiraceae|Dorea')]

    clades = [['Ruminococcaceae|unclassified', 'Bacteroidaceae|Bacteroides']]
    # clades = [('Bacteroidaceae|Bacteroides', 'Prevotellaceae|unclassified')]

    plot_clades_relationships(clades, './')



plot_clades()

# from preprocessing import faust_parser
# res = faust_parser.results()
# for r in res:
#     print r.clade_1 + ' + ' + r.clade_1

def format_stats(f):
    """
    Reads a file containing a copy of the MTV output
    :param f:
    """
    heuristics = []
    BIC_scores = []
    independent_models = []
    size_of_c = []
    iteration_time = []
    with open(f) as fd:
        for line in fd:
            if '\n' in line:
                line = line.replace('\n', '')
            chunks = line.split(' ')
            chunks = [c for c in chunks if c != '']
            heuristics.append(float(chunks[0]))
            BIC_scores.append(float(chunks[1]))
            #2 is query
            size_of_c.append(int(chunks[3]))
            independent_models.append(int(chunks[4]))
            iteration_time.append(float(chunks[5]))

    print 'heuristics =', heuristics
    print 'BIC_scores =', BIC_scores
    print 'independent_models =', independent_models
    print 'size_of_c =', size_of_c
    print 'iteration_time =', iteration_time

# format_stats('./output.txt')

def write_tree():
    from preprocessing.tree import Tree
    from preprocessing.parser import get_dataset
    ds=get_dataset()
    t = Tree(ds)
    xml=t.root.to_xml()
    with open('tree.xml', 'wb') as fd:
       fd.write(xml)

# write_tree()