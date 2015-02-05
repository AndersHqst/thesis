"""
Class and specialized functions to build and work with a bacteria family tree.
"""

import numpy as np
from utils.dataset_helpers import abundance_matrix

class Node(object):
    def __init__(self):
        super(Node, self).__init__()
        self.parent = None
        self.children = []
        self.name = ""
        self.depth = 0
        self.clades = ""
        # Numpy array of the abundance colum
        # w.r.t. the clade at a given leaf
        self.abundances = None


    def to_xml(self):
        xml = ''
        size = 1
        if self.is_root():

            tag_name = 'Root'
            # Attributes on root node?
            xml = '<%s name="nullRoot" size="%s">' % (tag_name, size)
            for child in self.children:
                xml += child.to_xml()
            xml += '</%s>' % tag_name

            return xml

        elif self.is_leaf():
            short_name = self.name.split('|')[-1]
            tag_name = 'depth_%d' % self.depth
            xml = '<%s name="%s" path="%s" size="%s" />' % (tag_name, short_name, self.clades, size)
            return xml

        else:
            short_name = self.name.split('|')[-1]
            tag_name = 'depth_%d' % self.depth
            xml = '<%s name="%s" path="%s" size="%s">' % (tag_name, short_name, self.clades, size)
            for child in self.children:
                xml += child.to_xml()
            xml += '</%s>' % tag_name

            return xml


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

    def __init__(self, ds):
        """
        Initialize a phylogenetic Tree for a given dataset.
        :param ds: Dataset
        :return: An initialized Tree
        """
        super(Tree, self).__init__()
        self.root = Node()
        self.root.name = 'Root'
        "Dataset related to the datasets"
        self.ds = ds
        # Submatrix of ds with bacteria abundances
        self.bacteria_abundances = None
        self.nodes = {}
        self.__build_bacteria_family_tree(self.ds)


    def __add_clades(self, node, clades, abundances, depth=0):
        """
        Recursively adds a list of clades to current datasets.
        :param node:
        :param clades:
        :return:
        """
        if depth < len(clades):

            # Unique name for the node includes the parent name
            # if not roow in the phylogenetic tree
            if depth == 0:
                name = clades[depth]
            else:
                name = clades[depth-1] + '|' + clades[depth]

            if not name in [n.name for n in node.children]:
                assert not (name in self.nodes), 'Attempting to add node twice'

                child = Node()
                child.name = name
                child.parent = node
                child.depth = depth + 1
                child.clades = '|'.join(clades[:depth+1])
                self.nodes[name] = child
                node.children.append(child)
                self.__add_clades(child, clades, abundances, depth + 1)
            else:
                child = [n for n in node.children if n.name == name][0]
                self.__add_clades(child, clades, abundances, depth + 1)

        # This is a leaf
        else:
            node.abundances = abundances


    def __build_bacteria_family_tree(self, ds):
        """
        Build the bacteria family datasets from a dataset.
        The data set is expected to be in the format of the datasets
        that can be created with bacteria parser, i.e. fir row from
        index [0][2:] hold bacterial clades
        row [1][2:] hold bacteria abundances
        :param ds: Daset with all know clades as columns.
        :return: Bacteria family datasets
        """
        self.ds = ds

        self.bacteria_abundances = abundance_matrix(np.array(ds))

        # Headers with clades
        bacteria_clades = ds[0][2:]

        # Insert all clades in the datasets
        for index, clade in enumerate(bacteria_clades):
            names = clade.split('|')
            if len(names) > 0:
                abundances = self.bacteria_abundances.T[index]
                # pass abundance as a column
                self.__add_clades(self.root, names, abundances.T)
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
            return column + node.abundances

        # This is not a leaf, so add all children
        for child in node.children:
            column = self.abundance_column_in_subtree(child, column)

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
            return nodes + [node]
        else:
            for child in node.children:
                nodes = self.nodes_at_max_depth(max_depth, child, depth + 1, nodes)
        return nodes


    def dataset_for_all_nodes(self):
        """
        Builds a dataset for all nodes
        :return:
        """
        nodes = self.nodes.values()
        return self.dataset_for_nodes(nodes)


    def dataset_at_max_depth(self, max_depth):
        """
        Returns a data w.r.t a max depth. Subtrees at max deth will have the
        abundances merge, and the clade name is create for the reached node.
        :param max_depth: Max depth in bacteria datasets.
        :return: Dataset at max_depth in the datasets
        :return:
        """
        nodes = self.nodes_at_max_depth(max_depth, self.root)
        return self.dataset_for_nodes(nodes)


    def dataset_for_clades(self, clade_names):
        """
        Returns a dataset of merged abundances for the clade names provided
        :param clade_names: A list of clade names.
        :return:
        """
        nodes = []
        for name in clade_names:
            if name in self.nodes:
                nodes.append(self.nodes[name])
            else:
                print 'Warning, no known clade with name: ', name

        return self.dataset_for_nodes(nodes)


    def dataset_for_nodes(self, nodes):
        """
        Returns a subset of the dataset used to build the tree, where leaf abundances are merged.
        :return: Dataset
        """

        abundance_columns = None
        headers = []

        for node in nodes:

            if not node.is_root():

                # The new header name is the clade at the node
                # 'Bacteria|Firmicutes|' from 'Bacteria|Firmicutes|Bacilli' if we
                # cut at some node, not leaf
                headers.append(node.name)

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


    def abundance_for_clade(self, clade_name):
        """
        Get the abundance row at a given clade.
        Important that calde names are given with the parent name
        if any ex: Firmicutes|Erysipelotrichi
        :param clade_name:
        :return:
        """
        assert clade_name and not (clade_name == ''), 'No clade name provided'
        assert clade_name in self.nodes, 'No node for clade_name'

        node = self.node_for_clade_name(clade_name)

        return self.abundance_column_in_subtree(node)


    def count_nodes(self, node=None, depth=0, count=0, count_depth=None):
        """
        Returns the number of nodes in the datasets
        :param node: Current node
        :param depth: Current depth
        :param count: Current count
        :param count_depth: Optional max depth for the count
        :return: Number of nodes in the datasets
        """
        if node is None:
            node = self.root

        for child in node.children:
            count = self.count_nodes(child, depth+1, count, count_depth)
        if count_depth is None or depth <= count_depth:
            return 1 + count
        return count

    def count_leafs(self, node=None, count=0):
        """
        Returns the number of leafs
        :param node: Current node
        :param count: Current count
        :return: Number of leafs in the datasets
        """
        if node is None:
            node = self.root

        if node.is_leaf():
            return 1 + count
        else :
            for child in node.children:
                count = self.count_leafs(child, count)

        return count


    def node_for_clade_name(self, clade_name):
        assert clade_name and not (clade_name == ''), 'No clade name provided'

        return self.nodes[clade_name]


    def nodes_have_same_lineage(self, node_a, node_b):
        """
        Returns true if node a and node b are in the same lineage
        :param node_a:
        :param node_b:
        :return:
        """
        return node_a.name in node_b.clades or node_b.name in node_a.clades

    def has_clade(self, clade_name):
        return clade_name in self.nodes

def test_tree():
    # Create a toy dataset, with the same .tab format as we use
    ds = [
        ['TID', 'STSite', 'Bacteria|Firmicutes|Bacilli', 'Bacteria|Firmicutes|Erysipelotrichi', 'Bacteria|Fusobacteria', 'unclassified'],
        [700107520, 'Tongue_dorsum',   0               ,               1                       ,            2           ,     7         ],
        [700107521, 'Tongue_dorsum',   10              ,              11                       ,           12           ,    19         ],
        [700107521, 'Tongue_dorsum',   20              ,              21                       ,           22           ,    99         ],

    ]

    tree = Tree()
    tree.build_bacteria_family_tree(ds)

    sub_ds = tree.dataset_at_max_depth(2)
    # Test be inspecting the result..
    print sub_ds

# test_tree()






