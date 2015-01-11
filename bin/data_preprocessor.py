#__author__ = 'Keyla'
import csv
import sys
from scipy.stats import tstd, gmean
import numpy as np

def get_otu(matrix, index):
    return get_otus(matrix)[index]

def get_otus(matrix):
    return matrix[0][4:-1]

def get_otu_abundances(matrix, otu):
        abundances =[]
        for row in range(1, len(matrix)):
            cur_abundance = int(float(matrix[row][otu]))
            abundances.append(cur_abundance)
        return abundances

def delete_otus_from_matrix(matrix, otus):
    new_matrix = []
    for row in range(0, len(matrix)):
        row_copy = []
        for column in range(0, len(matrix[0])):
            if column in otus:
                pass
            else:
                row_copy.append(matrix[row][column])
        new_matrix.append(row_copy)
    return new_matrix

def binary_to_otu(t, matrix):
    result = []
    otus = get_otus(matrix)
    for i, otu in enumerate(otus):
        if 2**i & t == 2**i:
            result.append(otu)
    return result

def loadData():
    '''The function load the stool dataset and translate it in to a matrix, all information is retained'''
    matrix = []
    with open('../data/Stool.csv', 'rb') as stool_csv:
        data_reader = csv.reader(stool_csv, delimiter=',')
        for row in data_reader:
            matrix.append(row)
    return np.array(matrix)

def abundance_matrix(matrix):
    """ Return the submatrix of abundance count. """
    # From row 1, from column 4 to second last
    return matrix[1:, 4:-1].astype(np.int)

def data_to_binary(matrix, otu_stat=None, number_of_otus=0):
    """ Descritises the matrix and returns a binary representation """
    binary_list = []
    for row in matrix:
        cur_binary = 0
        # Attribute indeces minus trailing new line character
        for i, value in enumerate(row):
            if number_of_otus != 0 and i >= number_of_otus:
                break
            if otu_stat == None:
                if value != 0:
                    cur_binary = cur_binary | 2 ** i
            else:
                if value >= otu_stat[i]:
                    cur_binary = cur_binary | 2 ** i
        binary_list.append(cur_binary)
    return binary_list


def otu_stats(matrix):
    otu_stats =[]
    for column in range(3,len(matrix[0])-1):
        cur_counts =[]
        for row in range(1,len(matrix)):
            cur_abundance = int(float(matrix[row][column]))
            cur_counts.append(cur_abundance)
        standart_div = tstd(cur_counts)
        mean = sum(cur_counts)/float(len(matrix)-1)
        otu_stats.append((mean, standart_div))
    print otu_stats
    return otu_stats

def otu_limits(matrix):
    lower_limits = []
    for row in matrix.T:
        Q_1 = np.percentile(row, 25)
        Q_3 = np.percentile(row, 75)
        IQR = Q_3-Q_1
        low = Q_1 - 1.5 * IQR
        upp = Q_3 + 1.5 * IQR
        if low > 0:
            print 'low: ', low
        abundances_without_outliers = []
        for i, value in enumerate(row):
            #if value <= upp and value >= low:
            if value >= low:
                abundances_without_outliers.append(value)
            else:
                print value
        stand_d = tstd(abundances_without_outliers)
        mean = np.mean(abundances_without_outliers)
        cur_lower = mean - 1.96 * stand_d
        #cur_lower = np.mean(abundances_without_outliers) - 2*tstd(abundances_without_outliers)
        if cur_lower < 0:
            cur_lower = 0
        lower_limits.append(cur_lower)
    return lower_limits


def data_cleaning(matrix):
    """Cleans the abundance matrix """
    #Removes otus which greatest abundance is 2 or lower
    clean_matrix = matrix.T[(matrix.T > 2).any(1),]
    #return cleaned_matrix
    return clean_matrix.T



matrix = loadData()
abundance_matrix = abundance_matrix(matrix)
#otu_stats(matrix)
#otu_limits(matrix)
data_cleaning(abundance_matrix)
lower_limits = otu_limits(abundance_matrix)
print lower_limits
print data_to_binary(abundance_matrix, otu_stat = lower_limits)


