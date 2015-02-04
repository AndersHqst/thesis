
from utils.dataset_helpers import *

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
            if val <= cand:
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

def maxent_discretization(dataset):

    # Get the abundance matrix and discretize it
    abundances = abundance_matrix(dataset).T
    discrete_matrix = []
    for row in abundances:
        threshold = find_threshold(row)
        discrete_row = []
        for val in row:
            if val < threshold:
                discrete_row.append(0)
            else:
                discrete_row.append(1)

        discrete_matrix.append(discrete_row)

    # transpose to dataset orientation
    discrete_matrix = np.array(discrete_matrix).T

    # Replace the abundance submatrix
    discretized_dataset = replace_abundance_matrix(dataset, discrete_matrix)

    return discretized_dataset


def median_discretization_row(row):
    """
    Discretize a list of numeric values by the median
    :param row:
    :param threshold:
    :return:
    """
    from utils.stats import median

    discrete_row = []
    threshold = median(row)

    for val in row:
        if val <= threshold:
            discrete_row.append(0)
        else:
            discrete_row.append(1)

    return threshold, discrete_row


def median_discretization(dataset):

    # Get the abundance matrix and discretize it
    abundances = abundance_matrix(dataset).T
    discrete_matrix = []
    for row in abundances:
        threshold, discrete_row = median_discretization_row(row)
        discrete_matrix.append(discrete_row)

    # transpose to dataset orientation
    discrete_matrix = np.array(discrete_matrix).T

    # Replace the abundance submatrix
    discretized_dataset = replace_abundance_matrix(dataset, discrete_matrix)

    return discretized_dataset


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
