#
#   Scratchpad for working with implementation from the root folder.
#

from matplotlib.pylab import plot, ylabel, xlabel, savefig, close, title, figtext

from plots.faust_result_discretized import plot_faust_relationships, plot_clades_relationships
from scipy.stats import pearsonr, spearmanr
from preprocessing.tree import Tree
from preprocessing.discretization import *
from preprocessing.preprocessors import remove_empty_samples, compute_relative_values, discrete_dataset_cleaning
import os


# clades = [['Burkholderiales|Alcaligenaceae', 'Synergistetes|Synergistia'],
# ['Flavobacteriales|unclassified', 'Synergistetes|Synergistia'],
# ['Veillonellaceae|Megamonas', 'Bacteria|Bacteroidetes'],
# ['Porphyromonadaceae|unclassified', 'Actinobacteria|Actinobacteria'],
# ['Actinomycetales|Corynebacteriaceae', 'Aeromonadales|Succinivibrionaceae'],
# ['Porphyromonadaceae|unclassified', 'Actinomycetales|Corynebacteriaceae'],
# ['Ruminococcaceae|Subdoligranulum', 'Ruminococcaceae|Ethanoligenens'],
# ['Erysipelotrichaceae|Coprobacillus', 'Peptococcaceae|Peptococcus'],
# ['Enterobacteriaceae|Escherichia/Shigella', 'Proteobacteria|Epsilonproteobacteria'],
# ['Alphaproteobacteria|Sphingomonadales', 'Bacteria|Cyanobacteria'],
# ['Ruminococcaceae|Subdoligranulum', 'Neisseriaceae|unclassified'],
# ['Veillonellaceae|Acidaminococcus', 'Pasteurellaceae|Aggregatibacter'],
# ['Victivallaceae|Victivallis', 'Coriobacteriaceae|unclassified'],
# ['Proteobacteria|Betaproteobacteria', 'Verrucomicrobiaceae|Akkermansia'],
# ['Anaeroplasmataceae|Asteroleplasma', 'Victivallaceae|Victivallis'],
# ['Fusobacteria|Fusobacteria', 'Firmicutes|unclassified'],
# ['Fusobacteria|Fusobacteria', 'Porphyromonadaceae|Dysgonomonas'],
# ['Coriobacteriaceae|Enterorhabdus', 'Verrucomicrobiaceae|Akkermansia'],
# ['Campylobacterales|Campylobacteraceae', 'Bacteria'],
# ['Firmicutes|unclassified', 'Actinobacteria|Actinomycetales']]

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



def build_summary_table():
    # Construct summary table
    pass


def evaluate_faust_in_model(model, body_site='Stool'):
    from preprocessing import faust_parser

    faust_results = faust_parser.results(body_site)

    # For each result in faust
    # translate clade names, to indeces
    #   create mtv query(headers) as a convenience
    #   let it throw a key error if header is unknown
    # crate table row with
    # key -/+ relationship faust pearson, spearman, association rules, in summary, agree? model phi


