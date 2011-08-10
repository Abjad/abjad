def _process_min_max_attribute(*min_max):
    '''Check and process min max attributes.
    The function expects at least one and at most two attributes.
    If only one attribute is given, this is taken as the maximum of a range.
    '''

    if len(min_max) == 0 or 2 < len(min_max):
        raise AttributeError('The function expects one or two attributes.')
    elif len(min_max) == 1:
        min = 0
        max = min_max[0]
    else:
        min = min_max[0]
        max = min_max[1]

    if not (min < max and isinstance(min, int) and isinstance(max, int)):
        raise AttributeError('Arguments must be integers and min < max.')

    return min, max
