class Component(object):

    def __init__(self):
        super(Component, self).__init__()
        self.nodes = 0
        self.itemsets = []

    def __str__(self):
        return 'nodes: %s components: ' % (bin(self.nodes), self.components)


class Graph(object):

    def __init__(self):
        super(Graph, self).__init__()

        # Nodes in a component
        self.components = []


    def add_node(self, itemset):
        """
        Add a new node to the graph. Components will be re-computed, and
        the itemset added to one component
        :param itemset:
        :return:
        """

        # Find all intersecting or disjoint components
        intersecting_components = []
        disjoint_components = []
        while 0 < len(self.components):
            component = self.components.pop()
            if component.nodes & itemset != 0:
                intersecting_components.append(component)
            else:
                disjoint_components.append(component)

        # Create new component as a merge of the added itemset
        # and intersecting components
        new_component = Component()
        new_component.nodes = itemset
        new_component.itemsets = [itemset]
        for intersecting_component in intersecting_components:
                new_component.nodes = new_component.nodes | intersecting_component.nodes
                new_component.itemsets += intersecting_component.itemsets

        self.components = disjoint_components + [new_component]


    def disjoint_summaries(self):
        """
        Iterator for disjoint summaries C
        """
        for component in self.components:
            yield component.itemsets

