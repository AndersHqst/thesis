#!/usr/bin/env python

import sys
import getopt
import pickle
import os
from utils.files import parse_dat_file
from utils.dataset_helpers import is_co_exclusion
import itemsets
from preprocessing.tree import Tree
import subprocess
from preprocessing import parser

dir = os.path.dirname(__file__)

def print_help(unknown_args=None):
    if not (unknown_args is None):
        print 'Unknown arguments: ', unknown_args
    print 'Use -o foldername for MTV results, and -d with a path to the dataset that was used.'
    sys.exit(2)


def parse_argv(argv):

    o = None
    d = None

    try:
        # Cmd line arguments.
        # Single letter arguments, args followed by ':' expect a value
        opts, args = getopt.getopt(argv, "o:d:")
    except getopt.GetoptError:
        print_help(argv)


    for opt, arg in opts:
        if opt in ("-o"):
            o = arg
        elif opt in ("-d"):
            d = arg

    if o is None or d is None:
        print_help()

    return os.path.join(dir, o), os.path.join(dir, d)


def main(argv):
    o, d = parse_argv(argv)

    # Parse the summary.txt that already holds the clade names, and
    # and the co-excluded pattern
    # This is not very pretty but the easiest way to the results
    dataset_file = open(d, 'rb')
    ds = pickle.load(dataset_file)

    # TODO: this will currently only work with the Stool.
    tree = Tree(parser.get_dataset())
    headers = ds[0][2:]

    summary = parse_dat_file(os.path.join(o, 'summary.dat'))

    # create output folder
    output_folder = os.path.join(o, 'phylogenetic-tree')
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for index, itemset in enumerate(summary):
        # Append extra set of headeres for negated values
        clade_names = itemsets.to_index_list(itemset, list(headers) + list(headers))
        co_ex = itemset >> len(headers)
        co_excluded_clade = ''
        if co_ex != 0:
            co_excluded_clade = itemsets.to_index_list(co_ex, list(headers) + list(headers))
        di_graph = tree.dot_graph_for_clades(clade_names, co_excluded_clade)
        file_name = os.path.join(output_folder, str(index))
        graph_file = file_name + '.dot'
        with open(graph_file, 'wb') as fd:
            fd.write(di_graph)

        png_file = file_name + '.png'

        subprocess.call(["dot", "-Tpng", graph_file, "-o", png_file])










if __name__ == '__main__':
    main(sys.argv[1:])
