"""
Parser scripts to parse hmp.lq.phylotype.filter.tab containing
a sample per colum that can come from any of the sample centers.
Rows are bacteria down to various depths of their family tree,
with their abundance counts for each sample
"""

import numpy as np

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
    import csv

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
    import csv

    dataset = dataset_at_bodyset('../../data/hmp.lq.phylotype.filter.tab', 'Stool')

    fd = open('../../data/Stool.tab', 'wb')

    csv_writer = csv.writer(fd, delimiter='\t')
    csv_writer.writerows(dataset)

    fd.close()

