#!/usr/bin/env pypy
#
#   Scratchpad for working with implementation from the root folder.
#

from matplotlib.pylab import plot, ylabel, xlabel, savefig, close, title, figtext
from preprocessing.discretization import *
from preprocessing.preprocessors import remove_empty_samples, compute_relative_values, discrete_dataset_cleaning
import os


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

def run_discretization_all_nodes():
    """
    TODO: Work in progress. Code to use a phylogenetic tree, and get a
    daset for the entire phylogenetic tree
    """
    from preprocessing import parser
    from preprocessing.tree import Tree
    from utils.dataset_helpers import abundance_matrix
    from itemsets import binary_vectors_to_ints
    from utils.files import write_dat_file

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

    # Write .dat file
    abundance = abundance_matrix(ds)
    D = binary_vectors_to_ints(abundance)
    write_dat_file('../experiments/1/Stool_maxent_discretized_all_nodes.dat', D)

    # Create a header file
    headers = []
    for header in ds[0][2:]:
        vals = header.split('|')
        if len(vals) > 1:
            headers.append('|'.join(vals[-2:]))
        else:
            headers.append(vals[0])

    with open('../experiments/2/stool_all_discrete.headers', 'wb') as fd:
        line = ' '.join(headers)
        fd.write(line)

# run_discretization_all_nodes()


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

def load_model():
    from mtv import MTV
    from utils.files import parse_dat_file
    from utils.files import parse_header_file

    D = parse_dat_file('../experiments/1/Stool_maxent_discretized_all_nodes.dat')
    headers = parse_header_file('../experiments/1/Stool_maxent_discretized_all_nodes.headers')
    summary = parse_dat_file('../experiments/1/summary.dat')
    mtv = MTV(D, summary, s=0.05)
    mtv.build_independent_models()

    return mtv




def evaluate_faust_in_model(body_site='Stool'):
    from preprocessing.parser import *
    from preprocessing.tree import Tree
    from preprocessing import faust_parser
    from scipy.stats import pearsonr, spearmanr
    from utils.correlation import phicoeff
    import itemsets
    from rule_miner import association_rule

    mtv = load_model()

    # For each result in faust
    # translate clade names, to indeces
    #   create mtv query(headers) as a convenience
    #   let it throw a key error if header is unknown
    # crate table row with
    # key -/+ relationship faust pearson, spearman, association rules, in summary, agree? model phi

    faust_results = faust_parser.results(body_site)

    ds = get_dataset('Stool')
    ds = compute_relative_values(ds)

    # Construct a tree to get abundances for faust results
    tree = Tree(ds)

    header = 'ID & relation ship & faust & pearson & spearman & pearson-phi & X -> & Y -> X & in C'

    for faust_result in faust_results:

        # make sure the faust result is in the tree
        # ex Clostridiales|IncertaeSedisXIV is not in the data set
        if not (tree.has_clade(faust_result.clade_1) and tree.has_clade(faust_result.clade_2)):
            continue

        clade_1 = faust_result.clade_1
        clade_2 = faust_result.clade_2

        # Get the nodes in the phylogenetic tree
        from_node = tree.node_for_clade_name(clade_1)
        to_node = tree.node_for_clade_name(clade_2)

        # Get the total abundance for the clades in the tree
        xs = tree.abundance_column_in_subtree(from_node)
        ys = tree.abundance_column_in_subtree(to_node)

        # Get faust correlations
        pearson = pearsonr(xs, ys)[0]
        spearman = spearmanr(xs, ys)[0]

        # Association rules
        # First, get the corresponding itemsets for the clades
        itemset_1 = itemsets.itemset_for_headers(clade_1, mtv.headers)
        itemset_2 = itemsets.itemset_for_headers(clade_2, mtv.headers)
        # Get association rules
        X_Y, Y_X = association_rule(mtv, itemset_1, itemset_2)

        # Get phi from model
        # that is, we need the counts for 00, 01, 10, 11. We will get these by the probabilities
        intersection = mtv.query_headers([clade_2, clade_1])
        _00 = len(mtv.D) * (1 - intersection)
        _01 = len(mtv.D) * (mtv.query_headers(clade_1) - intersection)
        _10 = len(mtv.D) * (mtv.query_headers(clade_2) - intersection)
        _11 = len(mtv.D) * (intersection)
        phi = phicoeff(_00, _01, _10, _11)

        line = '%d&' % faust_result.row

        line += '%s - %s &' % (clade_1, clade_2)

        line += '%d &' % faust_result.direction

        line += '%f&' % pearson

        line += '%f&' % spearman

        line += '%f&' % phi

        line += '%f,%f&' % (X_Y.confidence, X_Y.lift)

        line += '%s,%s&' % (Y_X.confidence, Y_X.lift)

        print line + '\\\\'


def clade_table(summary):
    from utils.files import parse_header_file
    from itemsets import to_index_list
    headers = parse_header_file('../experiments/1/Stool_maxent_discretized_all_nodes.headers')

    clades = []
    for binindex1, binindex2 in summary:
        clade1 = to_index_list(2**binindex1, headers)[0]
        clade2 = to_index_list(2**binindex2, headers)[0]
        clades.append((clade1, clade2))

    print 'clade 1 & clade 2'

    for clade1, clade2 in clades:
        print '%s & %s\\\\' % (clade1, clade2)

def clade_pair_abundances(summary):
    from utils.files import parse_header_file
    from itemsets import to_index_list
    from plots.clade_correlation import plot_clades_relationships
    headers = parse_header_file('../experiments/1/Stool_maxent_discretized_all_nodes.headers')

    clades = []
    for binindex1, binindex2 in summary:
        clade1 = to_index_list(2**binindex1, headers)[0]
        clade2 = to_index_list(2**binindex2, headers)[0]
        clades.append((clade1, clade2))

    plot_clades_relationships(clades, '../experiments/1/plots_top_10/')
