"""
Parser scripts to parse hmp.lq.phylotype.filter.tab containing
a sample per colum that can come from any of the sample centers.
Rows are bacteria down to various depths of their family tree,
with their abundance counts for each sample
"""

"""
RESULTS

Stool:
    353 rows - 2 header rows = 351 samples.
    Cleaning bacteria with only 2 or lower as max abundance -> 353, ie probably already cleaned
    removed all bacteria that never occur more than twice
    samples before cleaning:  355
    bacteria before cleaning:  728
    samples after cleaning:  355
    bacteria after cleaning:  189 # threshold 2
    bacteria after cleaning 130: threshold 10
    cleaned:  539


"""

import numpy as np
import csv
from matplotlib.pylab import plot, hist, ylabel, xlabel, show, savefig, close, title, axes, gcf
from faust_parser import  stool_results

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

    matrix = []


    # Pop the TID and STSite rows
    matrix.append(csv_reader.next())
    matrix.append(csv_reader.next())

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
        matrix.append([bacteria] + abundances)

    fd.close()

    # Convert and return transposed
    arr = np.array(matrix)

    return arr.T

def get_dataset(file_name):
    """
    Read the daset from file
    :param file_name:
    :return:
    """
    fd = open(file_name, 'rb')
    csv_reader = csv.reader(fd, delimiter='\t')
    matrix = []
    for index, row in enumerate(csv_reader):
        # header rows
        if index <= 1:
            matrix.append(row)
        # convert abundances
        else:
            id_cols = row[:2]
            abundances = [int(x) for x in row[2:]]
            matrix.append(id_cols + abundances)
    return np.array(matrix)

def dataset_at_bodyset(csv_file, bodysite):
    dataset = parse_dataset(csv_file)
    # Return row 1 with headers + sample at desired bodysite
    return np.vstack([dataset[:1], dataset[dataset[:,COLUMN_BODY_SITE] == bodysite]])


def bacteria_name(bacterial_clade):
    """
    Helper function to get the last descendent of a bacterial clade
    ex:
    Bacteria|Fusobacteria|Fusobacteria|Fusobacteriales|Fusobacteriaceae|Fusobacterium -> Fusobacterium
    Bacteria|Proteobacteria|Alphaproteobacteria|Rhizobiales|Methylocystaceae|unclassified -> Methylocystaceae
    :param bacterial_clade:
    :return:
    """

    if bacterial_clade == '':
        return bacterial_clade

    s = bacterial_clade.split('|')

    if s[-1] == 'unclassified' and len(s) > 1:
        return s[-2]

    return s[-1]

def save_stool_samples():
    """
    Helper function to save a stool sub-sample file to the data folder
    :return:
    """

    dataset = dataset_at_bodyset('../../data/hmp.lq.phylotype.filter.tab', 'Stool')

    fd = open('../../data/Stool.tab', 'wb')

    csv_writer = csv.writer(fd, delimiter='\t')
    csv_writer.writerows(dataset)

    fd.close()

def get_stool_dataset():
    """
    Helper fundtion to specifically read the stool dataset
    :return:
    """

    return get_dataset('../../data/Stool.tab')


def data_cleaning(dataset):
    """
    Remove bacteria with no abundance above 2
    :param dataset:
    :return:
    """

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



    # Remove bacteria with abundance count <= 2
    # transpose the zero sample matrix to iterate
    # bacterias as rows
    cleaned_dataset = []
    for index, row in enumerate(np.array(no_zero_samples).T):
        # Header rows
        if index < 2:
            cleaned_dataset.append(row)
        else:
            abundances = [int(x) for x in row[2:]]
            if not max(abundances) <= 2:
                cleaned_dataset.append(row)

    # Return the result, transposed to the original
    return np.array(cleaned_dataset).T

def abundance_matrix(matrix):
    """ Return the submatrix of abundance count.print 'rows before: ', len(dataset) - 2 """
    # From row 1, from column 2
    return matrix[1:, 2:].astype(np.int)


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

def plot_bacteria_hist(dataset, file_prefix, mid_quantile=False):
    """
    Saves a histogram of abundances binned
    :param dataset:
    :return:
    """
    for row in dataset.T[2:]:
        abundances = [float(x) for x in row[2:]]
        if mid_quantile:
            abundances.sort()
            abundances = abundances[int(len(abundances)*0.25): -int(len(abundances)*0.25)]
        print 'max abundance: ', max(abundances)
        xlabel('relative abundance bin')
        ylabel('#occurrences')
        bacteria_name = row[0]
        title(bacteria_name)
        hist(abundances, color='#0066FF')
        savefig('../../plots/hist/raw_mid_quantile/' + file_prefix + '-' + bacteria_name.replace('|', '_').replace('/','-'))
        close()

def run():
    ds = get_stool_dataset()
    ds = data_cleaning(ds)
    # ds = compute_relative_values(ds)

    # fd = open('../../data/Stool_normalized.tab', 'wb')
    # csv_writer = csv.writer(fd, delimiter='\t')
    # csv_writer.writerows(ds)
    plot_bacteria_hist(ds, 'stool_raw', mid_quantile=True)

    # print 'samples: ', len(ds)
    # print 'bacteria: ', len(ds[0])

# run()

###
### Plot abundances for Faust results
###
def columns_for_clade(headers, clade_name):
    indeces = []
    for index, header in enumerate(headers):
        if clade_name in header:
            indeces.append(index)
    return indeces

def plot_relationships():
    ds = get_stool_dataset()
    ds = data_cleaning(ds)
    ds = compute_relative_values(ds)

    faust_results = stool_results()
    for faust_result in faust_results:


        clades1 = faust_result.clade_1.split('-')
        origin = ''
        if 'unclassified' in clades1:
            origin = clades1[0]
        else:
            origin = '|'.join(clades1)

        clades2 = faust_result.clade_2.split('-')
        to = ''
        if 'unclassified' in clades2:
            to = clades2[0]
        else:
            to = '|'.join(clades2)

        xlabel('from')
        ylabel('to')
        title_text = 'Relationship: %d ' % faust_result.direction
        title(title_text)
        # find from-to bacteria abundances
        xs = []
        ys = []
        headers = ds[0][2:]
        for row in ds[1:]:
            for from_col in columns_for_clade(headers, origin):
                from_abundance = row[from_col]
                for to_col in columns_for_clade(headers, to):
                    to_abundance = row[to_col]
                    xs.append(from_abundance)
                    ys.append(to_abundance)

        # fig = gcf()
        # ax = fig.gca()
        # ax.set_yscale('log')
        # ax.set_xscale('log')

        # print 'Found %d relations' % len(xs)
        vals = zip(xs, ys)
        vals.sort()

        # vals = vals[:-20]
        plot([x for x,y in vals], [y for x,y in vals], 'bo', color='#0066FF')
        file_name = 'results_normalized/' + origin + '---' + to + '_' + str(faust_result.direction)
        # print '[RESULT] ', file_name
        # print vals
        savefig(file_name)
        close()


plot_relationships()
