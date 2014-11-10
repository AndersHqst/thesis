from charitems import to_binary, to_chars
from random import randint
from random import sample
from math import log

# Deciaml rounding issues
# https://docs.python.org/2/library/decimal.html
# from decimal import *
# getcontext().prec = 30

D = set([
        'abc',
        'abh',
        'abcdefgh',
        'abd',
        'abdf',
        'de',
        'def',
        'h',
        'gh',
        'e'
    ])

# create D samples
A = 'abcdefghijklmnopqrstu'
print 'legth of A:', len(A)
while len(D) != 200:
    _sample = sample(A, randint(0, len(A)))
    D.add(''.join(sorted(_sample)))

D = list(D)

for index, x in enumerate(D):
    D[index] = to_binary(x)
T  = 2 ** len(A)
# Dict for values u_x
U = {} 
C = set()
u0 = 2 ** -len(A)
print 'initial u0:', u0
# summary
ab = to_binary('ab')
gh = to_binary('gh')
de = to_binary('ghijlk')
fg = to_binary('abcdef')
# hijk = to_binary('fghab')
_sample = sample(A, randint(0, len(A)))
_sample = ''.join(sorted(_sample))
_def = to_binary(_sample)

C.union(set())
C.add(ab)
C.add(gh)
C.add(de)
C.add(fg)
# C.add(hijk)
for c in C:
    U[c] = 1.0


def contains(a, b):
    """ True if x contains t """
    return a & b == b

def model(t):
    res = 1.0
    for x in C:
        if contains(t, x):
            res = res * U[x]
    return u0 * res

def query(x):
    p = 0.0
    for t in range(T):
        if contains(t, x):
            p += model(t)
    return p

def fr(x):
    p = 0.0
    for xi in D:
        if contains(xi, x):
            p += 1
    p = p / float(len(D))
    assert p <= 1.0
    return p

def printU(U):
    for k in U:
        print to_chars(k) + ':' + str(U[k])

def iterative_scaling():
    global u0
    biggest_diff = -1
    converge_iterations = 0
    iterations = 0
    while iterations < 10: #((biggest_diff > 0.00000001 or biggest_diff == -1) and iterations < 100): # converge
        converge_iterations += 1
        biggest_diff = -1
        iterations += 1
        for x in C:

            p = query(x)
            U[x] = U[x] * (fr(x) / p) * ((1 - p) / (1 - fr(x)))
            u0 = u0 * (1 - fr(x)) / (1 -  p)

            diff = abs(fr(x) - query(x))
            if diff > biggest_diff:
                biggest_diff = diff
                # print 'biggest_diff:%f fx:%f p:%f' % (biggest_diff, fr(x), p)
    print 'Converge iterations:%d biggest_diff:%f ' % (converge_iterations, biggest_diff)

def run():
    """ Query all x in C subject to U """
    for x in C:
        print to_chars(x) + ':', query(x)


def running_example():
    # Summary from running example
    abc  = to_binary('abc') # 00000111
    cd   = to_binary('cd')  # 00001100
    _def = to_binary('def') # 00111000

    C.add(abc)
    C.add(cd)
    C.add(_def)

    # Initial computed values from running example in Mampey
    u0 = 2 ** -8
    u1 = u2 = u3 = 1
    U[abc] = u1
    U[cd] = u2
    U[_def] = u3
    print '\nInitial where abc=0.125'
    run()

    # Query with converged values
    u0 = 3 * 10 ** -4
    u1 = 28.5
    u2 = 0.12
    u3 = 85.4
    U[abc] = u1
    U[cd] = u2
    U[_def] = u3
    print '\nConverged:'
    run()


def s(C):
    global u0
    return -1 * (len(D) * (log(u0) +  sum([fr(x) * log(U[x]) for x in C]))) + 0.5 * len(C) * log(len(D))

# print 'frequency of %s: %f ' % (to_chars(ab), fr(ab))
iterative_scaling()
for c in C:
    print 'query %s with fr %f query %f ' % (to_chars(c), fr(c), query(c))
print 'query not in set %s with fr %f query %f ' % (to_chars(_def), fr(_def), query(_def))
print 'C', C
print 'u0', u0

def total_probability():
    total_prob = 0.0
    for t in range(T):
        p = model(t)
        # print 't: %s prob: %f' % (to_chars(t), p)
        # if p == u0:
        #     print 'prob of %s equals u0' % to_chars(t)
        total_prob += p
    print 'total prob: ', total_prob
total_probability()
cdf = to_binary('c')
print 'prop for no seen %s:%f' % (to_chars(cdf), query(cdf))
# for xi in X:
#     print '%s contains ab %d' % (to_chars(xi), contains(xi, ab))


