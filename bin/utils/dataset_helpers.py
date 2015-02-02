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