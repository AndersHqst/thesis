# Helper scripts to work with char itemsets
from charitems import to_binary, to_chars

def contains(x, t):
    """ True if x contains t """
    return x & t == t

def model(t):
    res = 1.0
    for x in C:
        if contains(x, t):
            res *= U[x]
    return u0 * res

def query(x):
    p = 0.0
    for t in range(T):
        if contains(t, x):
            p += model(x)
    return p

def run():
    for x in C:
        print to_chars(x) + ':', query(x)

T  = 2 ** 8 # abcdefgh

# Summary from running example
abc  = to_binary('abc') # 00000111
cd   = to_binary('cd')  # 00001100
_def = to_binary('def') # 00111000

C = set()
C.add(abc)
C.add(cd)
C.add(_def)

# Dict for values u_x
U = {} 

# Initial computed values from running example in Mampey
u0 = 2 ** -8
u1 = u2 = u3 = 1
U[abc] = u1
U[cd] = u2
U[_def] = u3
print '\nInitial where abc=0.123'
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



