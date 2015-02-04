#
#   Scratchpad for working with implementation from the root folder.
#

from matplotlib.pylab import plot, ylabel, xlabel, savefig, close, title, figtext

from plots.faust_result_discretized import plot_faust_relationships
from scipy.stats import pearsonr, spearmanr
from preprocessing.tree import Tree
from preprocessing.discretization import *
from preprocessing.preprocessors import remove_empty_samples, compute_relative_values, discrete_dataset_cleaning
import os


# plot_faust_relationships()
# run()


def run_discretization():
    """
    TODO: Work in progress. Code to use a phylogenetic tree, and get a
    daset at a particular depth.
    """
    from preprocessing import parser
    from preprocessing.tree import Tree
    from utils.dataset_helpers import abundance_matrix
    from itemsets import binary_vectors_to_ints
    from utils.files import write_dat_file

    ds = parser.get_dataset()
    ds = parser.compute_relative_values(ds)
    t = Tree(ds)
    bin_ds = t.dataset_at_max_depth(3)

    abundance = abundance_matrix(bin_ds)

    D = binary_vectors_to_ints(abundance)

    write_dat_file('../experiments/1/stool_depth3_discrete.dat', D)
    headers = []
    for header in bin_ds[0][2:]:
        vals = header.split('|')
        if len(vals) > 1:
            headers.append('|'.join(vals[-2:]))
        else:
            headers.append(vals[0])

    with open('../experiments/1/stool_depth3_discrete.headers', 'wb') as fd:
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



def evaluate_faust_in_model(mtv, body_site='Stool'):
    from preprocessing import faust_parser
    from matplotlib.pylab import plot, hist, ylabel, xlabel, savefig, close, title, figtext
    from preprocessing.parser import *
    from preprocessing.discretization import *
    from preprocessing.tree import Tree
    from preprocessing import faust_parser
    from scipy.stats import pearsonr, spearmanr
    from utils.correlation import phicoeff
    import itemsets
    from rule_miner import association_rule



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

    header = 'relation ship & faust & pearson & spearman & pearson-phi & X -> & Y -> X & in C'

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

        # Get disc correlation
        # disc_x, discrete_xs = median_discretization_row(xs)
        # disc_y, discrete_ys = median_discretization_row(ys)
        # phi = phicoeff(xs, ys)

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

        line = '%s - %s &' % (clade_1, clade_2)

        line += '%d &' % faust_result.direction

        line += '%f&' % pearson

        line += '%f&' % spearman

        line += '%f&' % phi

        line += '%f,%f&' % (X_Y.confidence, X_Y.lift)

        line += '%s,%s&' % (Y_X.confidence, Y_X.lift)

        print line


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


C = [[70, 125],
     [125, 126],
     [29, 72],
     [11, 108],
     [65, 170],
     [2, 190],
     [85, 97],
     [85, 104],
     [127, 186],
     [103, 149],
     [12, 195],
     [39, 128],
     [19, 124],
     [12, 177],
     [24, 141],
     [98, 147],
     [39, 195],
     [87, 163],
     [6, 8],
     [22, 90],
     [101, 107],
     [22, 101],
     [9, 71],
     [31, 55],
     [26, 86],
     [31, 194],
     [9, 26],
     [74, 107],
     [92, 129],
     [145, 153],
     [28, 49],
     [113, 165],
     [59, 137],
     [34, 102],
     [13, 167],
     [56, 98],
     [16, 59],
     [127, 150],
     [197, 198],
     [30, 139],
     [62, 131],
     [25, 33],
     [82, 181],
     [10, 87],
     [113, 192],
     [60, 174],
     [68, 178],
     [15, 166],
     [111, 197],
     [48, 191],
     [70, 108],
     [19, 136],
     [41, 123],
     [24, 45],
     [84, 144],
     [10, 58],
     [93, 154],
     [56, 172],
     [67, 79],
     [109, 181],
     [183, 187],
     [100, 161],
     [88, 110],
     [152, 183],
     [88, 152],
     [103, 140],
     [83, 185],
     [83, 100],
     [189, 199],
     [15, 54],
     [67, 148],
     [144, 191],
     [82, 173],
     [165, 184],
     [122, 138],
     [73, 193],
     [47, 78],
     [21, 190],
     [1, 168],
     [103, 164],
     [184, 197],
     [63, 141],
     [8, 176],
     [13, 52],
     [36, 49],
     [143, 165],
     [65, 133],
     [16, 171],
     [73, 121],
     [34, 167],
     [66, 117],
     [114, 168],
     [19, 40],
     [113, 118],
     [112, 179],
     [28, 111],
     [113, 116],
     [25, 125],
     [113, 115],
     [132, 189],
     [157, 179]]

clade_pair_abundances(C[:10])






