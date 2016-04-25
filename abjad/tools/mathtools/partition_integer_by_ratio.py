# -*- coding: utf-8 -*-
import sys


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
        message = 'is not integer-equivalent number: {!r}.'
        message = message.format(n)
        raise TypeError(message)

    ratio = mathtools.Ratio(ratio).numbers

    if not all(
        mathtools.is_integer_equivalent_number(part)
        for part in ratio
        ):
        message = 'some parts in {!r} not integer-equivalent numbers.'
        message = message.format(ratio)
        raise TypeError(message)

    result = [0]

    divisions = [
        float(abs(n)) * abs(part) / mathtools.weight(ratio)
        for part in ratio
        ]
    cumulative_divisions = mathtools.cumulative_sums(divisions, start=None)

    for division in cumulative_divisions:
        rounded_division = int(round(division)) - sum(result)
        #This makes rounding behave like python 2. Would be good to remove
        # in the long run
        if sys.version_info[0] == 3:
            if division - round(division) == 0.5:
                rounded_division += 1
        result.append(rounded_division)

    result = result[1:]

    # adjust signs of output elements
    if mathtools.sign(n) == -1:
        result = [-x for x in result]
    ratio_signs = [mathtools.sign(x) for x in ratio]
    result = [pair[0] * pair[1] for pair in zip(ratio_signs, result)]

    # return result
    return result
