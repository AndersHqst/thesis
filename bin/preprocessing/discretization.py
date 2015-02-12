
from utils.dataset_helpers import *


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


def maxent_discritization_threshold(row):
    from math import log

    maxent = 999999999999999999
    log_sums = []
    best_threshold = 0
    for val in row:

        threshold = val
        log_sum = 0
        for i in row:
            log_sum += log(abs(i-threshold)+0.1)

        log_sums.append(log_sum)

        if log_sum < maxent:
            maxent = log_sum
            best_threshold = val

    return best_threshold


def maxent_discretization_row(row):
    """
    Discretize a list of numeric values by the median
    :param row:
    :param threshold:
    :return:
    """
    from utils.stats import median

    discrete_row = []
    threshold = maxent_discritization_threshold(row)

    for val in row:
        if val <= threshold:
            discrete_row.append(0)
        else:
            discrete_row.append(1)

    return threshold, discrete_row


def maxent_discretization(dataset):

    # Get the abundance matrix and discretize it
    abundances = abundance_matrix(dataset).T
    discrete_matrix = []
    for row in abundances:
        threshold, discrete_row = maxent_discretization_row(row)
        discrete_matrix.append(discrete_row)

    # transpose to dataset orientation
    discrete_matrix = np.array(discrete_matrix).T

    # Replace the abundance submatrix
    discretized_dataset = replace_abundance_matrix(dataset, discrete_matrix)

    return discretized_dataset