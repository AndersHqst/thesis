
def parse_dat_file(path):
    """
    Parses a .dat file to a dataset of binary vectors
    represented by integers.
    The expected input file list binary position separated
    by spaces
    ex: 0 4 42 189\n
    :param path:
    :return:
    """
    D = []
    for line in open(path):
        clean_line = line.replace('\n', '')
        cmps = clean_line.split(' ')
        if 0 < len(cmps):
            bin_positions = [int(cmp) for cmp in cmps]
            val = 0
            for bp in bin_positions:
                val = val | 2 ** bp
            D.append(val)
    return D

def write_dat_file(file_name, data):
    import itemsets
    with open(file_name, 'wb') as fd:
        for X in data:
            line = ' '.join([str(x) for x in itemsets.to_index_list(X)]) + '\n'
            fd.write(line)