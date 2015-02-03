#
#   Scratchpad for working with implementation from the root folder.
#

from matplotlib.pylab import plot, ylabel, xlabel, savefig, close, title, figtext

from plots.faust_result_discretized import plot_relationships
from scipy.stats import pearsonr, spearmanr
from preprocessing.tree import Tree
from preprocessing.discretization import *
from preprocessing.preprocessors import remove_empty_samples, compute_relative_values
import os

# plot_relationships()
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
    # ds = parser.discretize_binary(ds)
    ds = remove_empty_samples(ds)
    t = Tree(ds, True)
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
    ds = maxent_discretization(ds)
    ds = remove_empty_samples(ds)

    # Build the phylogenetic tree, and
    # create dataset for all nodes
    t = Tree(ds, True)
    bin_ds = t.dataset_for_all_nodes()

    print 'all nodes, number of attributes: ', len(bin_ds[0]) - 2

    # Write .dat file
    abundance = abundance_matrix(bin_ds)
    D = binary_vectors_to_ints(abundance)
    write_dat_file('../experiments/1/Stool_maxent_discretized_all_nodes.dat', D)

    # Create a header file
    headers = []
    for header in bin_ds[0][2:]:
        vals = header.split('|')
        if len(vals) > 1:
            headers.append('|'.join(vals[-2:]))
        else:
            headers.append(vals[0])

    with open('../experiments/2/stool_all_discrete.headers', 'wb') as fd:
        line = ' '.join(headers)
        fd.write(line)

run_discretization_all_nodes()

def faust_results_to_parent_clade():
    # Find faust results and propagate clades up to some level
    # clades at this level could then be compared
    from preprocessing import faust_parser
    from preprocessing import parser

    max_clade_depth = 3

    results = faust_parser.results()
    ds = parser.get_dataset()
    tree = Tree(ds, False)

    correlation_nodes = []
    for faust_result in results:

        # Get nodes if they exist
        try:
            from_node = tree.node_for_clade_name(faust_result.clade_1)
            to_node = tree.node_for_clade_name(faust_result.clade_2)
        except KeyError, ke:
            continue

        if from_node.depth < max_clade_depth or to_node.depth < max_clade_depth:
            # No good
            print 'Ignoring nodes:'
            print from_node
            print to_node
            print 'faust_result: ', faust_result
            continue

        while from_node.depth > 3:
            from_node = from_node.parent

        while to_node.depth > 3:
            to_node = to_node.parent

        correlation_nodes.append((from_node, to_node))


        xlabel('from')
        ylabel('to')
        title_text = 'Relationship: %d ' % faust_result.direction
        title(title_text)
        # find from-to bacteria abundances
        xs = []
        ys = []
        discrete_xs = []
        discrete_ys = []

        # Get the total abundance for hte clades in the tree
        abundance_from = tree.abundance_column_in_subtree(from_node)
        abundance_to = tree.abundance_column_in_subtree(to_node)

        # List the in-sample values for each sample
        for index, _row in enumerate(ds[1:]):
            from_abundance = abundance_from[index]
            to_abundance = abundance_to[index]

            xs.append(from_abundance)
            ys.append(to_abundance)

            discrete_xs.append(discrete_value(abundance_from, from_abundance))
            discrete_ys.append(discrete_value(abundance_to, to_abundance))

        try:
            pearson = pearsonr(xs, ys)
            spearman = spearmanr(xs, ys)

            if pearson > 0.5:
                pass
            correlation_coef = 'Pearson: (%.3f,%.3f), Spearman: (%.3f,%.3f)' % (pearson[0], pearson[1], spearman[0], spearman[1])
            correlation_coef += ' sample points: %d' % len(xs)
            figtext(0.01, 0.01, correlation_coef, fontsize=10)
        except Exception, e:
            print e
            print 'Faust result: ', faust_result.id
            print 'clades1: ', from_node.name
            print 'clades2: ', to_node.name
            print 'xs: %s', xs
            print 'ys: %s', ys


        disc_x = discrete_relative_threshold(xs)
        disc_y = discrete_relative_threshold(ys)
        # plot discretization lines
        a, b = [disc_x, disc_x], [0, max(ys)]
        c, d = [0, max(xs)], [disc_y, disc_y]
        plot(a, b, c='r')
        plot(c, d, c='r')

        # write discrete results onto plot
        pairs = zip(discrete_ys, discrete_xs)
        _00 = '00: ' + str(len([x for x in pairs if x == (0,0)]))
        _01 = '01: ' + str(len([x for x in pairs if x == (0,1)]))
        _10 = '10: ' + str(len([x for x in pairs if x == (1,0)]))
        _11 = '11: ' + str(len([x for x in pairs if x == (1,1)]))
        figtext(0.7, 0.85, _00, fontsize=10)
        figtext(0.7, 0.80, _01, fontsize=10)
        figtext(0.7, 0.75, _10, fontsize=10)
        figtext(0.7, 0.70, _11, fontsize=10)

        from_depth = 'From depth: %d' % from_node.depth
        to_depth = 'To depth: %d' % to_node.depth
        figtext(0.7, 0.65, from_depth, fontsize=10)
        figtext(0.7, 0.60, to_depth, fontsize=10)

        same_lineage = 'False'
        if tree.nodes_have_same_lineage(from_node, to_node):
            same_lineage = ' True'
        figtext(0.7, 0.55, 'Same lineage: ' + same_lineage, fontsize=10)


        # vals = vals[:-20]
        plot(xs, ys, 'g.', color='#0066FF')
        file_name = '../../experiments/1/faust_results/' +str(faust_result.id) + '_' + from_node.name.replace('|', '-') + '---' + to_node.name.replace('|', '-') + '_' + str(faust_result.direction)
        file_name = os.path.join(dir, file_name)
        # print '[RESULT] ', file_name
        # print vals
        savefig(file_name)
        close()

# faust_results_to_parent_clade()



