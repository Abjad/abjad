# -*- coding: utf-8 -*-


def cumulative_sums(sequence, start=0):
    r'''Cumulative sums of `sequence`.

    ::

        >>> mathtools.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8], start=None)
        [1, 3, 6, 10, 15, 21, 28, 36]

    Returns list.
    '''

    if start is None:
        result = []
    else:
        result = [start]

    for element in sequence:
        if result:
            new = result[-1] + element
            result.append(new)
        else:
            result.append(element)

    return result
