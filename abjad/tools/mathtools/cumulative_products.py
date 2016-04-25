# -*- coding: utf-8 -*-


def cumulative_products(sequence):
    r'''Cumulative products of `sequence`.

    ::

        >>> mathtools.cumulative_products([1, 2, 3, 4, 5, 6, 7, 8])
        [1, 2, 6, 24, 120, 720, 5040, 40320]

    ::

        >>> mathtools.cumulative_products([1, -2, 3, -4, 5, -6, 7, -8])
        [1, -2, -6, 24, 120, -720, -5040, 40320]

    Raises type error when `sequence` is neither list nor tuple.

    Raises value error on empty `sequence`.

    Returns list.
    '''

    if not isinstance(sequence, (list, tuple)):
        raise TypeError

    if len(sequence) == 0:
        raise ValueError

    result = [sequence[0]]
    for element in sequence[1:]:
        result.append(result[-1] * element)

    return result
