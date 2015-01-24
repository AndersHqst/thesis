"""
A set of helper functions for working with itemsets represented as integers
"""

from utils.memoisation import memoise

def contains(a, b):
    """ True if a contains b """
    return a & b == b

def singletons_of_itemsets(itemsets):
    singletons = set()
    for itemset in itemsets:
        val = itemset
        pos = 0
        while val != 0:
            if val & 1 == 1:
                singletons.add(2 ** pos)
            val = val >> 1
            pos += 1
    return singletons

def singletons(D):
    """
    Finds all singletons present in a dataset D and adds them to a set I.
    All rows in D are or'ed together to create a bit mask of all attributes.
    These are then all read as the 1 bit in the mask being shifted right
    :param I: Set singletons are added to
    :param D: Dataset where singletons will be taken from
    :return:
    """

    # Mask all bits observed in D
    mask = 0
    for d in D:
        mask = mask | d

    # Create set of singletons for all 1 bits
    return singletons_of_itemsets([mask])

def to_index_list(itemset):
    """
    Returns a sorted list of the binary indeces of 1's
    found in the itemset
    :param itemset:
    :return: List of binary indeces i itemset
    """
    l = []
    pos = 0
    while itemset != 0:
        if itemset & 1 == 1:
            l.append(pos)
        itemset = itemset >> 1
        pos += 1
    return l

def to_index_lists(itemsets):
    """
    Use to_index_list on every itemset in the passed in
    itemsets and returns them in a list
    """
    l = []
    for itemset in itemsets:
        l.append(to_index_list(itemset))
    return l

def union_of_itemsets(itemsets):
    """Union of items in itemsets"""
    result = 0
    for c in itemsets:
        result = c | result
    return result

@memoise
def singletons_of_itemset(itemset):
    singletons = []
    val = itemset
    pos = 0
    while val != 0:
        if val & 1 == 1:
            singletons.append(2 ** pos)
        val = val >> 1
        pos += 1
    return singletons

