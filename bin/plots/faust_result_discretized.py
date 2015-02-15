from matplotlib.pylab import plot, hist, ylabel, xlabel, savefig, close, title, figtext, grid, scatter
from preprocessing.parser import *
from preprocessing.discretization import *
from preprocessing.tree import Tree
from preprocessing import faust_parser
from scipy.stats import pearsonr, spearmanr
from utils.correlation import phicoeff_lists

def plot_faust_relationships(relative_values=True):

    ds = get_dataset('Stool')

    if relative_values:
        ds = compute_relative_values(ds)

    # Use numeric Tree. We will discreteze relevant values ourselves
    # and plot the numeric correlations
    tree = Tree(ds)

    # Plot all relations in the faust results
    faust_results = faust_parser.results('Stool')
    for faust_result in faust_results:

        # if faust_result.number_of_supporting_methods < 5:
        #     continue

        # make sure the faust result is in the tree
        # ex Clostridiales|IncertaeSedisXIV is not in the data set

        if not (tree.has_clade(faust_result.clade_1) and tree.has_clade(faust_result.clade_2)):
            continue

        # Get the nodes in the phylogenetic tree
        from_node = tree.node_for_clade_name(faust_result.clade_1)
        to_node = tree.node_for_clade_name(faust_result.clade_2)

        title_text = 'Relative clade abundances'
        title(title_text)
        # find from-to bacteria abundances
        xs = []
        ys = []

        # Get the total abundance for hte clades in the tree
        abundance_from = tree.abundance_column_in_subtree(from_node)
        abundance_to = tree.abundance_column_in_subtree(to_node)

        # List the in-sample values for each sample
        for index, _row in enumerate(ds[1:]):
            from_abundance = abundance_from[index]
            to_abundance = abundance_to[index]

            xs.append(from_abundance)
            ys.append(to_abundance)

        grid(True)
        text_x = 0.67

        sample_points = 'Sample points: %d' % len(xs)
        figtext(text_x, 0.85, sample_points, fontsize=10)

        from_clade = from_node.name.replace('|', '-')
        to_clade = to_node.name.replace('|', '-')
        xlabel(from_clade, fontsize=10)
        ylabel(to_clade, fontsize=10)

        disc_x, discrete_xs = median_discretization_row(xs)
        disc_y, discrete_ys = median_discretization_row(ys)

        # plot discretization lines
        a, b = [disc_x, disc_x], [0, max(ys)]
        c, d = [0, max(xs)], [disc_y, disc_y]
        plot(a, b, c='r')
        plot(c, d, c='r')



        # Discrete bin sizes
        pairs = zip(discrete_ys, discrete_xs)
        _00 = '00: ' + str(len([x for x in pairs if x == (0,0)]))
        _01 = '01: ' + str(len([x for x in pairs if x == (0,1)]))
        _10 = '10: ' + str(len([x for x in pairs if x == (1,0)]))
        _11 = '11: ' + str(len([x for x in pairs if x == (1,1)]))
        figtext(text_x, 0.82, _00, fontsize=10)
        figtext(text_x, 0.79, _01, fontsize=10)
        figtext(text_x, 0.76, _10, fontsize=10)
        figtext(text_x, 0.73, _11, fontsize=10)
        phi = 'phi: %f' % phicoeff_lists(discrete_xs, discrete_ys)
        figtext(text_x, 0.70, phi, fontsize=10)

        # Depth of nodes in the phylogenetic tree
        from_depth = 'x depth: %d' % from_node.depth
        to_depth = 'y depth: %d' % to_node.depth
        figtext(text_x, 0.67, from_depth, fontsize=10)
        figtext(text_x, 0.64, to_depth, fontsize=10)

        # Discretization values
        median_x = 'median x: %f' % disc_x
        median_y = 'median y: %f' % disc_y
        figtext(text_x, 0.61, median_x, fontsize=10)
        figtext(text_x, 0.58, median_y, fontsize=10)

        # Same lineage
        same_lineage = 'False'
        if tree.nodes_have_same_lineage(from_node, to_node):
            same_lineage = ' True'
        figtext(text_x, 0.55, 'Same lineage: ' + same_lineage, fontsize=10)

        # Faust et al result
        faust = 'Faust result: %d' % faust_result.direction
        figtext(text_x, 0.52, faust, fontsize=10)

        # Pearson and spearman correlations
        try:
            pearson = pearsonr(xs, ys)
            spearman = spearmanr(xs, ys)

            pearson = 'Pearson: %.3f, %.3f' % (pearson[0], pearson[1])
            spearman = 'Spearman: %.3f, %.3f' % (spearman[0], spearman[1])

            figtext(text_x, 0.49, pearson, fontsize=10)
            figtext(text_x, 0.46, spearman, fontsize=10)
        except Exception, e:
            print e
            print 'Faust result: ', faust_result.id
            print 'clades1: ', from_node.name
            print 'clades2: ', to_node.name
            print 'xs: %s', xs
            print 'ys: %s', ys

        # Plot values
        scatter(xs, ys, s=1, color='#0066FF')

        # Save the figure to file
        file_name = '../../plots/plots/stool_normalized_clade/' +str(faust_result.id) + '_' + from_clade + '---' + to_clade + '_' + str(faust_result.direction)
        file_name = os.path.join(dir, file_name)
        savefig(file_name)
        close()
