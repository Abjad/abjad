# -*- encoding: utf-8 -*-


def partition_integer_by_ratio(n, ratio):
    r'''Partitions positive integer-equivalent `n` by `ratio`.

    ::

        >>> mathtools.partition_integer_by_ratio(10, [1, 2])
        [3, 7]

    Partitions positive integer-equivalent `n` by `ratio` with negative parts:

    ::

        >>> mathtools.partition_integer_by_ratio(10, [1, -2])
        [3, -7]

    Partitions negative integer-equivalent `n` by `ratio`:

    ::

        >>> mathtools.partition_integer_by_ratio(-10, [1, 2])
        [-3, -7]

    Partitions negative integer-equivalent `n` by `ratio` with negative parts:

    ::

        >>> mathtools.partition_integer_by_ratio(-10, [1, -2])
        [-3, 7]

    Returns result with weight equal to absolute value of `n`.

    Raises type error on noninteger `n`.

    Returns list of integers.
    '''
    from abjad.tools import mathtools

    if not mathtools.is_integer_equivalent_number(n):
        raise TypeError('input "%s" is not integer-equivalent number.' % n)

    if not all(mathtools.is_integer_equivalent_number(part) for part in ratio):
        raise TypeError('some parts in "%s" not integer-equivalent numbers.' % ratio)

    result = [0]

    divisions = [float(abs(n)) * abs(part) / mathtools.weight(ratio) for part in ratio]
    cumulative_divisions = mathtools.cumulative_sums(divisions)

    for division in cumulative_divisions:
        rounded_division = int(round(division)) - sum(result)
        result.append(rounded_division)

    result = result[1:]

    # adjust signs of output elements
    if mathtools.sign(n) == -1:
        result = [-x for x in result]
    ratio_signs = [mathtools.sign(x) for x in ratio]
    result = [pair[0] * pair[1] for pair in zip(ratio_signs, result)]

    # return result
    return result
