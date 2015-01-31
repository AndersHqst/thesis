import numpy as np

def abundance_matrix(matrix):
    """ Return the submatrix of abundances"""
    # From row 1, from column 2
    try:
        return matrix[1:, 2:].astype(np.int)
    except:
        pass
    return matrix[1:, 2:].astype(np.float)
