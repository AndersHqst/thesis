#__author__ = 'Keyla'
import csv
import sys


def get_attribute(index, A):
    attribute = A.get(index)
    return attribute

def get_attributes(t,A):
    otus = []
    for a in A:
        if 2^a and t:
            otus.append(get_attribute(a, A))


def loadData():
    '''The function load the stool dataset and translate it in to a matrix, all information is retained'''
    matrix = []
    with open('../data/Stool.csv', 'rb') as stool_csv:
        data_reader = csv.reader(stool_csv, delimiter=',')
        for row in data_reader:
            matrix.append(row)
    return matrix

def data_to_binary(matrix):
    '''The funktions turn a matrix into a list of strings that represent the binary representation
    together with the number of attributes'''
    binary_list = []
    for row in range(1,len(matrix)):
        cur_binary_string =''
        cur_binary = 0
        binary_position = 0
        # Attribute indeces minus trailing new line character
        for column in range(3,len(matrix[0]) - 1):
            try:
                binary = int(float(matrix[row][column]))
            except ValueError:
                print 'That was no valid number.' , matrix[row][column], row
                exit(0)
            if (int(float(matrix[row][column])) == 0):
                pass
            else :
                cur_binary = cur_binary | 2**binary_position
            binary_position+=1
        binary_list.append(cur_binary)
    return binary_list

matrix = loadData()
print data_to_binary(matrix)






