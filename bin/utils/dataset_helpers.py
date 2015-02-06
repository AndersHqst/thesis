import numpy as np

def abundance_matrix(matrix):
    """ Return the submatrix of abundances"""
    # From row 1, from column 2
    try:
        return matrix[1:, 2:].astype(np.int)
    except:
        pass
    return matrix[1:, 2:].astype(np.float)


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


def dataset_with_negations(dataset, singletons):
        """
        Returns a dataset with negated attributes added.
        Every row in the dataset, will have bit-flipped version
        of itself, added as a left shift of the number of singletons

        Ex a dataset with binary 1001, 1110 will be returned as 01101001, 00011110
        :param dataset: List of integers representing binary transactions
        :return: Data set with negated attributes
        """
        dataset_with_negations = []
        for X in dataset:
            positive_attributes = len(singletons)
            mask = (2 ** positive_attributes) - 1
            negated_attributes = (mask ^ X) << positive_attributes
            row = X | negated_attributes
            dataset_with_negations.append(row)

        return dataset_with_negations


def is_mutual_exclusion(itemset, singletons):
    """
    :param itemset: Itemset
    :param singletons: All singleton, positive and negated
    :return: True if the itemset includes a negated attribute
    and tuple of (positive (values, negated_value), or False and (0.0)
    """

    negated_attribute = itemset >> int(len(singletons) / 2.0)
    positive_attributes = itemset ^ negated_attribute

    if negated_attribute != 0:
        return (True, (positive_attributes, negated_attribute))

    return (False, (0,0))
