"""
Parser scripts to parse hmp.lq.phylotype.filter.tab containing
a sample per colum that can come from any of the sample centers.
Rows are bacteria down to various depths of their family tree,
with their abundance counts for each sample
"""

"""
RESULTS

Stool:
    354 rows - 2 header rows = 351 samples.
    Cleaning bacteria with only 2 or lower as max abundance -> 353, ie probably already cleaned
    removed all bacteria that never occur more than twice
    samples before cleaning:  355
    bacteria before cleaning:  728
    samples after cleaning:  355
    bacteria after cleaning:  189 # threshold 2
    bacteria after cleaning 130: threshold 10
    cleaned:  539

    Full bacteria datasets has 1054 nodes.
    Bacteria, unclassified, Archaea as the roots.
    If we only take top 3 levels we are down to dept index 4, we only have 182 nodes
    depth index 3 gives 79 nodes


"""
import os
dir = os.path.dirname(__file__)
import numpy as np
import csv
from matplotlib.pylab import plot, hist, ylabel, xlabel, show, savefig, close, title, axes, gcf, figtext
from faust_parser import  results
from scipy.stats import pearsonr, spearmanr
from datasets.tree import Tree
from utils.dataset_helpers import abundance_matrix
from math import ceil
from scipy.stats import tvar

COLUMN_TID = 0
COLUMN_BODY_SITE = 1
# In the transposed matrix, beyond the first two columns are
# bacterial clades

def parse_dataset(csv_file):
    """
    Returns transposed numpy array of the dataset with abundance levels transformed to int
    These are the samples that can be found in hmp.lq.phylotype.filter.tab

    One sample is arranged per column, and a row represents a bacteria.
    Cells contain abundance counts.
    :param csv_file:
    :return:
    """

    fd = open(csv_file, 'rb')
    csv_reader = csv.reader(fd, delimiter='\t')

    # Pop the TID and STSite rows
    matrix = np.array(csv_reader.next())
    matrix = np.vstack([matrix, csv_reader.next()])

    # Read in entire matrix and transform abundance values
    # these are in the sub block from index row:2 col:1
    for row in csv_reader:
        bacteria = row[0]
        abundances = []
        for x in row[1:]:
            val = 0
            if x != '':
                val = int(x)
            abundances.append(val)
        new_row = np.array([bacteria] + abundances)
        matrix = np.vstack([matrix, new_row])

    fd.close()

    # Return a transposed matrix as
    # we work with samples as rows
    return matrix.T

def dataset_at_bodyset(csv_file, bodysite):
    dataset = parse_dataset(csv_file)
    # Return row 1 with headers + sample at desired bodysite
    return np.vstack([dataset[:1], dataset[dataset[:,COLUMN_BODY_SITE] == bodysite]])


def save_sample(bodysite='Stool'):
    """
    Helper function to save a stool sub-sample file to the data folder
    :return:
    """
    faust_file = os.path.join(dir, '../../data/hmp.lq.phylotype.filter.tab')
    dataset = dataset_at_bodyset(faust_file, bodysite)

    file_name = os.path.join(dir, '../../data/%s.tab' % bodysite)

    fd = open(file_name, 'wb')

    csv_writer = csv.writer(fd, delimiter='\t')
    csv_writer.writerows(dataset)

    fd.close()


def get_dataset(bodysite='Stool'):
    """
    Read the daset from file
    :param file_name:
    :return:
    """
    file_name = os.path.join(dir, '../../data/%s.tab' % bodysite)
    fd = open(file_name, 'rb')
    csv_reader = csv.reader(fd, delimiter='\t')
    # header rows
    matrix = np.array(csv_reader.next())
    matrix = np.vstack([matrix, csv_reader.next()])
    for index, row in enumerate(csv_reader):
        id_cols = row[:2]
        abundances = [int(x) for x in row[2:]]
        new_row = np.array(id_cols + abundances)
        matrix = np.vstack([matrix, new_row])
    return data_cleaning(matrix)

def remove_empty_samples(dataset):
    # remove 0 samples
    no_zero_samples = []
    for index, row in enumerate(dataset):
        # Header rows
        if index < 2:
            no_zero_samples.append(row)
        else:
            sample_abundances = [int(x) for x in row[2:]]
            if max(sample_abundances) > 0:
                no_zero_samples.append(row)

    return no_zero_samples

def data_cleaning(dataset):

    no_zero_samples = remove_empty_samples(dataset)

    # Remove bacteria with abundance count <= 2
    # transpose the zero sample matrix to iterate
    # bacterias as rows
    cleaned_dataset = []
    for index, row in enumerate(np.array(no_zero_samples).T):
        # Header rows
        if index < 2:
            cleaned_dataset.append(row)
        else:
            abundances = [int(x) for x in row[1:]]
            if not max(abundances) <= 2:
                cleaned_dataset.append(row)

    # Return the result, transposed to the original
    return np.array(cleaned_dataset).T


def compute_relative_values(dataset):
    """
    Returns a matrix with relative abundance counts, relative
    to the sample size.
    :param matrix:
    :return: Relative abundance matrix
    """

    # Keep headers
    relative_matrix = [list(dataset[0])]

    # relative per sample!
    # Skip row with headers
    for row in dataset[1:]:
        abundances = [int(x) for x in row[2:]]
        total = sum(abundances)
        new_row = list(row[:2])
        for value in abundances:
            new_row.append(value / float(total))
        relative_matrix.append(list(new_row))

    return np.array(relative_matrix)


###
### Plot abundances for Faust results
###
def columns_for_clade(headers, clade_name):
    indeces = []
    # print 'Bacteria for cladename: ', clade_name
    for index, header in enumerate(headers):
        if clade_name in header:
            # print 'header [%d]: %s' % (index, header)
            indeces.append(index)
    # print '\n'
    return indeces

def replace_abundance_matrix(dataset, replacement):
    """
    Replace the abundance matrix of a dataset
    :param dataset: Dataset
    :param replacement: Replacement for abundance matrix
    :return:
    """
    clade_names = np.array(dataset[0][2:])
    ds = np.vstack((clade_names, replacement))

    # Attach sample columns, on left side
    left_columns = np.array(dataset)[:,0:2]
    ds = np.hstack((left_columns, ds))

    return ds

def find_threshold(vals):
    from scipy.stats import entropy
    candidates = vals
    lowest_entropy = 999999999
    lowest_threshold = None
    highest_entropy = 0
    highest_threshold = None
    entropies = []
    thresholds = []
    for cand in candidates:
        disc_vals = []
        for val in vals:
            if val < cand:
                disc_vals.append(0)
            else:
                disc_vals.append(1)
        prob_0 = [x for x in disc_vals if x == 0]
        prob_1 = [x for x in disc_vals if x == 1]
        prob_0 = [1/float(len(prob_0)) for x in prob_0]
        prob_1 = [1/float(len(prob_1)) for x in prob_1]
        if len(prob_0) > 10 and len(prob_1) > 10:
            ent = entropy(prob_0 + prob_1)
            if ent < lowest_entropy:
                lowest_entropy = ent
                lowest_threshold = cand
            if ent > highest_entropy:
                highest_entropy = ent
                highest_threshold = cand
            entropies.append(ent)
            thresholds.append(cand)
    # print 'discrete values 0: %d 1: %d' % (len(prob_0), len(prob_1))
    # plot(thresholds, entropies)
    # return lowest_threshold, lowest_entropy, highest_threshold, highest_entropy

    return highest_threshold


def discrete_relative_threshold(row, threshold=0.5):
    return find_threshold(row)

    # row_sorted = sorted(row)
    # outliers = int(ceil(len(row_sorted) * 0.05))
    # if outliers < len(row_sorted):
    #     row_sorted = row_sorted[:-outliers]
    # return max(row_sorted) * threshold


def discrete_value(row, value, threshold=0.5):
    b = discrete_relative_threshold(row, threshold)
    if value <= b:
        return 0
    return 1

def discrete_abundances(row, threshold=0.5):

    discrete_row = []

    if 0 < len(row):
        for val in row:
            discrete_row.append(discrete_value(row, val, threshold))

    return discrete_row


def discretize_binary(dataset):

    # Get the abundance matrix and discretize it
    abundances = abundance_matrix(dataset).T
    discrete_matrix = []
    for row in abundances:
        discrete_matrix.append(discrete_abundances(row))
    discrete_matrix = np.array(discrete_matrix).T

    # Replace the abundance submatrix
    discretized_dataset = replace_abundance_matrix(dataset, discrete_matrix)

    return discretized_dataset

# ds = get_dataset('Stool')
# ds = data_cleaning(ds)
# ds = compute_relative_values(ds)
# ds = discretize_binary(ds, 0.15)
# write_tab_file('../../data/Stool_disc.tab', ds)



def plot_relationships(relative_values=True):

    ds = get_dataset('Stool')

    if relative_values:
        ds = compute_relative_values(ds)

    # Use numeric Tree. We will discreteze relevant values ourselves
    # and plot the numeric correlations
    tree = Tree(ds, False)

    # Plot all relations in the faust results
    faust_results = results('Stool')
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

            # discrete_xs.append(discrete_value(abundance_from, from_abundance))
            # discrete_ys.append(discrete_value(abundance_to, to_abundance))

        # print 'xs: ', xs
        # exit()
        # Uncomment to use log axis
        # fig = gcf()
        # ax = fig.gca()
        # ax.set_yscale('log')
        # ax.set_xscale('log')

        # print 'Found %d relations' % len(xs)
        # vals = zip(xs, ys)
        # vals.sort()
        # vals = filter(lambda (x,y): x != 0 or y != 0, vals)
        # vals.sort(reverse=True)
        # print vals
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
        file_name = '../../plots/plots/stool_normalized_clade/' +str(faust_result.id) + '_' + from_node.name.replace('|', '-') + '---' + to_node.name.replace('|', '-') + '_' + str(faust_result.direction)
        file_name = os.path.join(dir, file_name)
        # print '[RESULT] ', file_name
        # print vals
        savefig(file_name)
        close()


def plot_bacteria_hist(dataset, folder, mid_quantile=False):
    """
    Saves a histogram of abundances binned
    :return:
    """

    # Get the transposed abundances matrix
    abundances = abundance_matrix(dataset).T

    # Get header names to priint on the plots
    headers = dataset[0][2:]

    for index, bacteria_column  in enumerate(abundances):

        abundances = [float(x) for x in bacteria_column]

        if mid_quantile:
            abundances.sort()
            abundances = abundances[int(len(abundances)*0.25): -int(len(abundances)*0.25)]

        xlabel('relative abundance bin')
        ylabel('#occurrences')

        bacteria_name = headers[index]
        title(bacteria_name)
        bins, intervals, patches = hist(abundances, color='#0066FF')

        # Write discretized values
        threshold = 0.5
        discretized_abundances = discrete_abundances(abundances, threshold=threshold)
        _0 = '0: ' + str(len([x for x in discretized_abundances if x == 0]))
        _1 = '1: ' + str(len([x for x in discretized_abundances if x == 1]))

        relatve_threshold = discrete_relative_threshold(abundances, threshold)
        threshold_text = 'Threshold: %f' % relatve_threshold
        figtext(0.7, 0.90, threshold_text, fontsize=10)
        figtext(0.7, 0.85, _0, fontsize=10)
        figtext(0.7, 0.80, _1, fontsize=10)

        # Draw threshold line
        a, b = [relatve_threshold, relatve_threshold], [0, max(bins)]
        plot(a, b, c='r')

        # Write max and avg
        max_abundance = 'max: %f' % max(abundances)
        avg_abundance = 'avg: %f' % (sum(abundances) / float(len(abundances)))
        figtext(0.7, 0.75, max_abundance, fontsize=10)
        figtext(0.7, 0.70, avg_abundance, fontsize=10)

        # write variance
        variance = 'var: %f' % tvar(abundances)
        figtext(0.7, 0.65, variance, fontsize=10)

        # Save fig to folder
        folder_path = os.path.join(dir, '../../experiments/' + folder)
        if not (os.path.exists(folder_path)):
            os.makedirs(folder_path)
        savefig(folder_path + '-' + bacteria_name.replace('/','-').replace('|', '-'))

        close()

def run():
    ds = get_dataset()
    # ds = compute_relative_values(ds)
    tree = Tree(ds, False)
    ds = tree.dataset_at_max_depth(3)
    plot_bacteria_hist(ds, '1/hists_absolute/')

