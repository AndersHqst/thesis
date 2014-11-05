from charitems import to_binary
from mtv import *

def test():
    a = to_binary('a')
    abc = to_binary('abc')
    bc = to_binary('bc')
    bcd = to_binary('bcd')
    assert contains(abc, bc)
    assert contains(abc, a)
    assert contains(abc, bcd) == False
    assert contains(abc, bcd) == False
    assert contains(bc, a) == False

def test_charify():
    a = to_chars(1)
    assert a == 'a', a
    abc = to_chars(7)
    assert abc == 'abc', abc

test()
test_charify()