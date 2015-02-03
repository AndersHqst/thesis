from matplotlib.pylab import plot, hist, ylabel, xlabel, savefig, close, title, figtext
from preprocessing.parser import *
from preprocessing.discretization import *
from preprocessing.tree import Tree
from preprocessing import faust_parser
from scipy.stats import pearsonr, spearmanr
from utils.correlation import phicoeff

def plot_faust_relationships(relative_values=True):

    ds = get_dataset('Stool')

    if relative_values:
        ds = compute_relative_values(ds)

    # Use numeric Tree. We will discreteze relevant values ourselves
    # and plot the numeric correlations
    tree = Tree(ds, False)

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

        xlabel('from')
        ylabel('to')
        title_text = 'Relationship: %d ' % faust_result.direction
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


        disc_x = find_threshold(xs)
        disc_y = find_threshold(ys)
        discrete_xs = []
        for x in xs:
            if x <= disc_x:
                discrete_xs.append(0)
            else:
                discrete_xs.append(1)
        discrete_ys = []
        for x in ys:
            if x <= disc_y:
                discrete_ys.append(0)
            else:
                discrete_ys.append(1)
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
        phi = 'phi: %f' % phicoeff(discrete_xs, discrete_ys)
        figtext(0.7, 0.65, phi, fontsize=10)

        from_depth = 'From depth: %d' % from_node.depth
        to_depth = 'To depth: %d' % to_node.depth
        figtext(0.7, 0.60, from_depth, fontsize=10)
        figtext(0.7, 0.55, to_depth, fontsize=10)

        same_lineage = 'False'
        if tree.nodes_have_same_lineage(from_node, to_node):
            same_lineage = ' True'
        figtext(0.7, 0.50, 'Same lineage: ' + same_lineage, fontsize=10)


        # vals = vals[:-20]
        plot(xs, ys, 'g.', color='#0066FF')
        file_name = '../../plots/plots/stool_normalized_clade/' +str(faust_result.id) + '_' + from_node.name.replace('|', '-') + '---' + to_node.name.replace('|', '-') + '_' + str(faust_result.direction)
        file_name = os.path.join(dir, file_name)
        # print '[RESULT] ', file_name
        # print vals
        savefig(file_name)
        close()

def plot_clades_relationships(clade_pairs):

    ds = get_dataset('Stool')
    ds = compute_relative_values(ds)

    # Use numeric Tree. We will discreteze relevant values ourselves
    # and plot the numeric correlations
    tree = Tree(ds, False)

    for clade_1, clade_2 in clade_pairs:


        # Get the nodes in the phylogenetic tree
        from_node = tree.node_for_clade_name(clade_1)
        to_node = tree.node_for_clade_name(clade_2)

        xlabel('from')
        ylabel('to')
        title_text = '%s --- %s' % (clade_1, clade_2)
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
            print 'clades1: ', from_node.name
            print 'clades2: ', to_node.name
            print 'xs: %s', xs
            print 'ys: %s', ys


        disc_x = find_threshold(xs)
        disc_y = find_threshold(ys)
        discrete_xs = []
        for x in xs:
            if x <= disc_x:
                discrete_xs.append(0)
            else:
                discrete_xs.append(1)
        discrete_ys = []
        for x in ys:
            if x <= disc_y:
                discrete_ys.append(0)
            else:
                discrete_ys.append(1)
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
        phi = 'phi: %f' % phicoeff(discrete_xs, discrete_ys)
        figtext(0.7, 0.65, phi, fontsize=10)

        from_depth = 'From depth: %d' % from_node.depth
        to_depth = 'To depth: %d' % to_node.depth
        figtext(0.7, 0.60, from_depth, fontsize=10)
        figtext(0.7, 0.55, to_depth, fontsize=10)

        same_lineage = 'False'
        if tree.nodes_have_same_lineage(from_node, to_node):
            same_lineage = ' True'
        figtext(0.7, 0.50, 'Same lineage: ' + same_lineage, fontsize=10)


        # vals = vals[:-20]
        plot(xs, ys, 'g.', color='#0066FF')
        file_name = '../../experiments/1/plots/' + from_node.name.replace('|', '-').replace('/', '%') + '---' + to_node.name.replace('|', '-').replace('/', '%')
        file_name = os.path.join(dir, file_name)
        # print '[RESULT] ', file_name
        # print vals
        savefig(file_name)
        close()