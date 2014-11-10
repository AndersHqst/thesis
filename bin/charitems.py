""" 
    Helper scripts to work with char itemsets represented in binary
"""

def to_binary(string):
    """
    Converts anchar itemset string to a binary representation e.g.
    'a'   -> 1 (0001)
    'b'   -> 2 (0010)
    'aba' -> 3 (0011)
    ... 
    """

    # Remove dublicate chars
    string = ''.join(set(string))

    int_rep = 0
    for s in string:
        # eg 'c' should have position 3 from the right in a bit string: 0100
        # magic 97 is because ord(a) = 98
        bit_position = ord(s) - 97

        # eg bit_position = 3 -> 2**3 -> 6 -> 0100 = bit_value
        bit_value = 2 ** bit_position

        # set the bit_value, since string is a set, 
        # we know this bit has not been set before and is 0
        # eg 1001 | 0010 = 1011
        int_rep = int_rep | bit_value
    # print "Converted '%s' to binary: %s" % (string, bin(int_rep))
    return int_rep


def to_chars(binary):
    """ Converts binary representations of an char itemset to a string """
    string = ""
    for t in range(100):
        bit = 2 ** t
        if binary & bit == bit:
            char_val = t + 97
            string += str(unichr(char_val))
    return string