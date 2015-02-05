def median(vals):
    """
    Return the median value from a list of numerical values
    :param vals: List of values
    :return:
    """
    from math import ceil
    sorted_vals = sorted(vals)
    mid_index = int(ceil(len(sorted_vals) / 2.0)) - 1
    if len(vals) % 2 == 1:
        return sorted_vals[mid_index]
    else:
        return (sorted_vals[mid_index] + sorted_vals[mid_index+1]) / 2.0

