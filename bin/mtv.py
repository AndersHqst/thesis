from charitems import to_binary, to_chars
from random import randint
from random import sample
from math import log
from itertools import combinations
from time import time
from memoisation import memoise
from Block import Block
from time import time

# Sample
D = list()

# Summary:
C = set()

#Maximum description length
k = 8

# Set of all attributes:
A = 'abcdefghijkl'
# print 'Attributes (%d): %s' % (len(A), A)

# Set of singletons
I = set()
for a in A:
    I.add(to_binary(a))

def create_patterns(attributes, patterns, size):       
    """Creates all patterns of a given size and add them to patterns"""
    comb = combinations(A,size)
    for c in comb:
        pattern = to_binary(''.join(c))
        patterns.add(pattern)

patterns = set()
#add all itemsets of size 2 and 3 to patterns:
# create_patterns(A, patterns, 2)
create_patterns(A, patterns, 2)
create_patterns(A, patterns, 3)

print 'patterns: ', len(patterns)
# #Add all singletons to sumary:
# create_patterns(A, C, 1)

# Generate random sample D
while len(D) != 500:
    _sample = sample(A, randint(1, len(A)))
    D.append(''.join(sorted(_sample)))
print 'D (%d): %s' % (len(D), D)

for index, x in enumerate(D):
    D[index] = to_binary(x)

# Initialise sample space
T  = 2 ** len(A)

# Dict for values U_x
U = {}

def total_probability(T_c):
    """ Assert and print the total probability of the model """
    total_prob = 0.0
    for T in T_c:
        p = model(T, C, u0, U)
        total_prob += p
    # assert abs(total_prob - 1.0) < 0.001, "Total probability was: %f " % total_prob
    print 'total prob: ', total_prob


def contains(a, b):
    """ True if a contains b """
    return a & b == b

def union_of_itemsets(itemsets):
    """Union of items in itemsets"""
    result = 0
    for c in itemsets:
        result = c | result
    return result

def model(T, C, u0, U):
    res = 1.0
    for x in C:
        if contains(T.union_of_itemsets, x):
            res = res * U[x]
    return u0 * res * T.block_weight

def c_partition(C, partition):
    C_copy = C.copy()
    for X in C:
        for p in partition:
            # intersection is not empty
            if not X & p == 0:
                C_copy.remove(X)
                return c_partition(C_copy, partition.union([X]))
    return partition

build_blocks_time_a = 0
build_blocks_time_b = 0
call_model_time = 0
def query(x, C, u0, U):
    global build_blocks_time_a
    global build_blocks_time_b
    global call_model_time

    start = time()
    # Compute blocks
    T_c = compute_blocks(C.union([x]))
    build_blocks_time_a += time() - start
    start = time()

    compute_block_weights(T_c, U)
    build_blocks_time_b += time() - start

    start = time()
    p = 0.0
    for T in T_c:
        if contains(T.union_of_itemsets, x):
            p += model(T, C, u0, U)
    assert p != 0, "p was 0"
    call_model_time += time() - start
    return p

# Memoise: The function will cache previous results with the argument
# this assumes that D does not change between cached results.
@memoise
def fr(x):
    p = 0.0
    for xi in D:
        if contains(xi, x):
            p += 1
    p = p / float(len(D))
    assert p <= 1.0
    return p

def h(x, y):
    """
    Heurestic for scoring an itemset
    :param x:
    :param y:
    :return:
    """
    b = 0
    if y == 0.0 or y == 1.0 or x == 1.0:
        b = 0
    else:
        b = (1 - x) * log( (1-x) / (1-y))
    a = 0
    if y != 0:
        a = x * log(x / y)
    return  a + b


def find_best_itemset_mampey(X, Y, Z, C, u0, U):
    """
    TODO: How to use this? It is not clear from Mampey how to initialize
    where X and Z are initially empty
    :param X: itemset
    :param Y: remaining itemsets
    :param Z: currently best itemset
    :return:
    """
    fr_X = fr(X)
    p_X = query(X, C, u0, U)
    fr_Z = fr(Z)
    p_Z = query(Z, C, u0, U)
    h_X = h(fr_X, p_X)
    h_Z = h(fr_Z, p_Z)
    if h_X > h_Z:
        Z = X
    XY = union_of_itemsets([X, union_of_itemsets(Y)])
    fr_XY = fr(XY)
    p_XY = query(XY, C, u0, U)
    b = max(h(fr_X, p_XY), h(fr_XY, p_X))
    if b > h_Z and len(to_chars(X)) <= 3:
        Y_iterable = Y.copy()
        for y in Y_iterable:
            Y = Y - set([y])
            Z = find_best_itemset_mampey(union_of_itemsets([X, y]), Y, Z, C, u0, U)
    # else:
        # print 'pruned branch'
    return Z


# @memoise_set
block_cache = {}
def compute_blocks(_C):
    """Compute the set of blocks that C infer
        return: Topologically sorted blocks T_C
    """

    key = tuple(sorted(_C))
    if key in block_cache:
        return block_cache[key]

    T_c = list()
    T_unions = set()

    # iterate the combination sizes in reverse
    for i in range(len(_C)+1)[::-1]:
        choose = i
        for comb in combinations(_C, choose):
            union = union_of_itemsets(comb)
            if not union in T_unions:
                T_unions.add(union)
                T = Block()
                T.union_of_itemsets = union
                T.itemsets = set(comb)
                T_c.append(T)


    block_cache[key] = T_c
    return T_c

def compute_block_sizes(T_c):
    for T in T_c:
        T.cummulative_block_size = 2 ** (len(A) - len(to_chars(T.union_of_itemsets)))
    for i, Ti in enumerate(T_c):
        Ti.block_size = Ti.cummulative_block_size
        for Tj in T_c[:i]:
            if Ti < Tj:
                Ti.block_size = Ti.block_size - Tj.block_size
    return T_c

block_weights_a = 0
block_weights_b = 0
def compute_block_weights(T_c, U):
    global block_weights_a
    global block_weights_b
    start = time()
    for T in T_c:
        T.cummulative_block_weight = 1
        # Iterate all I
        for i in I:
            if contains(T.union_of_itemsets, i):
                T.cummulative_block_weight *= U[i]
            else:
                T.cummulative_block_weight *= (1 + U[i])
    block_weights_a += time() - start
    start = time()
    for i, Ti in enumerate(T_c):
        Ti.block_weight = Ti.cummulative_block_weight
        for Tj in T_c[:i]:
            if Ti < Tj:
                Ti.block_weight = Ti.block_weight - Tj.block_weight
    block_weights_b += time() - start

def iterative_scaling(C):
    U = {}
    u0 = 2 ** -len(A)
    biggestdiff = -1
    for c in C.union(I):
        U[c] = 1.0
    converge_iterations = 0
    iterations = 0
    print 'iterative scaling with len of C ', len(C.union(I))
    start = time()

    while iterations < 20: #((biggest_diff > 0.00000001 or biggest_diff == -1) and iterations < 100): # converge
        converge_iterations += 1
        biggest_diff = -1
        iterations += 1
        for x in C.union(I):

            p = query(x, C, u0, U)
            U[x] = U[x] * (fr(x) / p) * ((1 - p) / (1 - fr(x)))
            u0 = u0 * (1 - fr(x)) / (1 -  p)

            # diff = abs(fr(x) - p)
            # if diff > biggest_diff:
                # biggest_diff = diff
                # print 'biggest_diff:%f fx:%f p:%f' % (biggest_diff, fr(x), p)

    # print 'Converge iterations:%d biggest_diff:%f ' % (converge_iterations, biggest_diff)
    return u0, U

# sorted_patterns = list(patterns)[::-1]
# sorted_pattern = filter(lambda x: fr(x) >= 1, sorted_patterns)
def find_best_itemset(C, u0, U):
    """Returns a pattern that potentially will be included in the summary."""
    # return patterns.pop();
    Z = None
    best = -1
    removable = set()
    for X in patterns:
        fr_X = fr(X)
        p_X = query(X, C, u0, U)
        h_X = h(fr_X, p_X)
        if h_X > best:
            best = h_X
            Z = X
        if h_X <= 0.0:
            print "heurestic of zero remove? h:", h_X

            # print "Itemset already predicted exactly, remove!"

    patterns.remove(Z)
    return Z

def MTV():
    """ """
    global C
    global u0
    global U

    u0 = 2 ** -len(A)
    for c in C.union(I):
        U[c] = 1.0

    # Compute our initial, current best, model
    # X = find_best_itemset(C, u0, U)
    X = find_best_itemset_mampey(0, I, 0, C, u0, U)
    C = C.union([X])
    u0, U = iterative_scaling(C)


    # This is the current best score
    cur_score = s(C, u0, U)

    # Brute force all patterns
    while len(patterns) > 0 and len(C) < k:

        # Possible best itemset to include in the summary
        start = time()
        # X = find_best_itemset(C, u0, U)
        X = find_best_itemset_mampey(0, I, 0, C, u0, U)
        print 'Found best itemset: ', time() - start

        # Candidate summary 
        _C = C.union([X])
        
        # Candidate model
        start = time()
        _u0, _U = iterative_scaling(_C)
        print 'iterative scaling: ', time() - start
        
        # Candidate score
        temp_score = s(_C, _u0, _U)

        # If the score has improved, we use the 
        # candidate summary as our
        # current best summary
        if  temp_score < cur_score:
            cur_score = temp_score
            C = _C
            u0 = _u0
            U = _U
        else:
            print "score did not decrease, break"
            break

def s(C, u0, U):
    return -1 * (len(D) * (log(u0) +  sum([fr(x) * log(U[x]) for x in C]))) + 0.5 * len(C) * log(len(D))


start = time()
MTV()
print 'MTV run time: ', time() - start
print 'Final summary: '
for x in C:
    print to_chars(x)

for c in C:
    print 'query %s with fr %f query %f uX: %f' % (to_chars(c), fr(c), query(c, C, u0, U), U[c])
print 'u0: ', u0

# Building time
print 'Build blocks a: ', build_blocks_time_a
print 'Build blocks b: ', build_blocks_time_b
print 'Call model: ', call_model_time
print 'Block weights a,', block_weights_a
print 'Block weights b,', block_weights_b

def is_in_sumamry(y, C):
    for x in C:
        if y == x:
            return True
    return False

def query_unknowns(amount):
    """Attempts to create an amount of itemsets not in the summary, and
        print their frequency and estimated frequency
        amount: Amount of itemsets not in C to attempt to find
    """
    unknowns = 0
    for t in range(T):
        y = randint(0, T)
        if not is_in_sumamry(y, C) and len(to_chars(y)) <= 3:
            unknowns += 1
            print 'Unknown itemset: %s with fr %f query %f' % (to_chars(y), fr(y), query(y, C, u0, U))
        if unknowns == amount:
            return

query_unknowns(10)

T_c = compute_blocks(C)
compute_block_weights(T_c, U)

total_probability(T_c)


print 'compute blocks (%d): print union and itemsets' % len(T_c)
print 'Transactions: ', T - 1
print 'summary: ', [to_chars(itemset) for itemset in C]
compute_block_weights(T_c, U)
for T in T_c:
    print T, [to_chars(itemset) for itemset in T.itemsets]

