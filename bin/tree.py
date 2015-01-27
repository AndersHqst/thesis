"""
Class and spezialized functions to build and work with a bacteria family tree.
"""

import numpy as np
from parsers.bacteria_parser import abundance_matrix

class Node(object):
    def __init__(self):
        super(Node, self).__init__()
        self.parent = None
        self.children = []
        self.name = ""
        self.clades = ""
        # Numpy array of the abundance colum
        # w.r.t. the clade at a given leaf
        self.abundances = None

    def is_leaf(self):
        """
        Note: only leaf nodes hold a abundance column
        :return: True if this is a leaf node
        """
        return (self.abundances is None) == False

    def is_root(self):
        return self.parent is None

    def __str__(self):
        return self.name


class Tree(object):

    def __init__(self):
        super(Tree, self).__init__()
        self.root = Node()
        self.root.name = 'Root'
        "Dataset related to the tree"
        self.ds = None
        # Submatrix of ds with bacteria abundances
        self.bacteria_abundances = None


    def add_clades(self, node, clades, abundances, depth=0):
        """
        Recursively adds a list of clades to current tree.
        :param node:
        :param clades:
        :return:
        """
        if depth < len(clades):
            name = clades[depth]
            if not name in [n.name for n in node.children]:
                child = Node()
                child.name = name
                child.parent = node
                child.clades = '|'.join(clades[:depth+1])
                node.children.append(child)
                self.add_clades(child, clades, abundances, depth + 1)
            else:
                child = [n for n in node.children if n.name == name][0]
                self.add_clades(child, clades, abundances, depth + 1)
        # This is a leaf
        else:
            node.abundances = abundances


    def build_bacteria_family_tree(self, ds):
        """
        Build the bacteria family tree from a dataset.
        The data set is expected to be in the format of the datasets
        that can be created with bacteria parser, i.e. fir row from
        index [0][2:] hold bacterial clades
        row [1][2:] hold bacteria abundances
        :param ds: Daset with all know clades as columns.
        :return: Bacteria family tree
        """
        self.ds = ds

        self.bacteria_abundances = abundance_matrix(np.array(ds))

        # Headers with clades
        bacteria_clades = ds[0][2:]

        # Insert all clades in the tree
        for index, clade in enumerate(bacteria_clades):
            names = clade.split('|')
            if len(names) > 0:
                abundances = self.bacteria_abundances.T[index]
                # pass abundance as a column
                self.add_clades(self.root, names, abundances.T)
            else:
                print 'bad column: ', names
        return self.root


    def abundance_column_in_subtree(self, node, column=None):
        """
        Returns the abundance column for a subtree.
        This is the sum of all abundance columns in the subtree

        :param node: Subtree root node
        :param column: Current subtree column
        :return: Column with abundances for the subtree
        """
        if column is None:
            # init 0 column with as many dimensions as in the abundance matrix
            column = np.array([0 for val in range(len(self.bacteria_abundances))])
            column = column.T

        # Leaf node, return the abundance column
        if not (node.abundances is None):
            return node.abundances

        # This is not a leaf, so add all children
        for child in node.children:
            column = column + self.abundance_column_in_subtree(child, column)

        return column


    def nodes_at_max_depth(self, max_depth, node, depth=0, nodes=None):
        """
        Return nodes at a max depth, or leafs if these are before max depth.
        :param max_depth: Max depth
        :param node: Starting node
        :param depth: Optional. Current depth
        :param nodes: Optional. Current nodes found
        :return:
        """
        if nodes is None:
            nodes = []

        if max_depth <= depth or node.is_leaf():
            return [node]
        else:
            for child in node.children:
                nodes = nodes + self.nodes_at_max_depth(max_depth, child, depth + 1, nodes)
        return nodes


    def dataset_at_max_depth(self, max_depth):
        """
        Returns a data w.r.t a max depth. Subtrees at max deth will have the
        abundances merge, and the clade name is create for the reached node.
        :param max_depth: Max depth in bacteria tree.
        :return: Dataset at max_depth in the tree
        """

        abundance_columns = None
        headers = []

        for node in self.nodes_at_max_depth(max_depth, self.root):

            if not node.is_root():

                # The new header name is the clade at the node
                # 'Bacteria|Firmicutes|' from 'Bacteria|Firmicutes|Bacilli' if we
                # cut at some node, not leaf
                headers.append(node.clades)

                # Get the merged abundance columns for the subtree from the node
                column = self.abundance_column_in_subtree(node)

                # A bit of juggling here, the column is a row here
                column = np.array([column]).T

                if abundance_columns is None:
                    abundance_columns = column
                else:
                    abundance_columns = np.hstack((abundance_columns, column))

        # attach header row on top of abundances
        headers = np.array(headers)
        dataset = np.vstack((headers, abundance_columns))

        # Attach sample columns, on left side
        left_columns = np.array(self.ds)[:,0:2]
        dataset = np.hstack((left_columns, dataset))


        return dataset


    def count_nodes(self, node, depth=0, count=0, count_depth=0):
        """
        Returns the number of nodes in the tree
        :param node: Current node
        :param depth: Current depth
        :param count: Current count
        :param count_depth: Optional max depth for the count
        :return: Number of nodes in the tree
        """
        for child in node.children:
            count = self.count_nodes(child, depth+1, count, count_depth)
        if depth <= count_depth:
            return 1 + count
        return count


def test_tree():
    # Create a toy dataset, with the same .tab format as we use
    ds = [
        ['TID', 'STSite', 'Bacteria|Firmicutes|Bacilli', 'Bacteria|Firmicutes|Erysipelotrichi', 'Bacteria|Fusobacteria', 'unclassified'],
        [700107520, 'Tongue_dorsum',   0               ,               1                       ,            2           ,     7         ],
        [700107521, 'Tongue_dorsum',   10              ,              11                       ,           12           ,    19         ],

    ]

    tree = Tree()
    tree.build_bacteria_family_tree(ds)

    sub_ds = tree.dataset_at_max_depth(10)
    print sub_ds

test_tree()