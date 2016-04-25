# -*- coding: utf-8 -*-


def partition_integer_into_units(n):
    r'''Partitions positive integer into units:

    ::

        >>> mathtools.partition_integer_into_units(6)
        [1, 1, 1, 1, 1, 1]

    Partitions negative integer into units:

    ::

        >>> mathtools.partition_integer_into_units(-5)
        [-1, -1, -1, -1, -1]

    Partitions ``0`` into units:

    ::

        >>> mathtools.partition_integer_into_units(0)
        []

    Returns list of zero or more parts with absolute value equal to ``1``.
    '''
    from abjad.tools import mathtools

    result = abs(n) * [mathtools.sign(n) * 1]

    return result
