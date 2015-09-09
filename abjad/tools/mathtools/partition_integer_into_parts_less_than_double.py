# -*- coding: utf-8 -*-
from __future__ import print_function


def partition_integer_into_parts_less_than_double(n, m):
    r'''Partitions integer `n` into parts less than double integer `m`.

    ..  container:: example

        ::

            >>> for n in range(1, 24+1):
            ...     print(n, mathtools.partition_integer_into_parts_less_than_double(n, 4))
            1 (1,)
            2 (2,)
            3 (3,)
            4 (4,)
            5 (5,)
            6 (6,)
            7 (7,)
            8 (4, 4)
            9 (4, 5)
            10 (4, 6)
            11 (4, 7)
            12 (4, 4, 4)
            13 (4, 4, 5)
            14 (4, 4, 6)
            15 (4, 4, 7)
            16 (4, 4, 4, 4)
            17 (4, 4, 4, 5)
            18 (4, 4, 4, 6)
            19 (4, 4, 4, 7)
            20 (4, 4, 4, 4, 4)
            21 (4, 4, 4, 4, 5)
            22 (4, 4, 4, 4, 6)
            23 (4, 4, 4, 4, 7)
            24 (4, 4, 4, 4, 4, 4)

    Returns tuple of one or more integers.
    '''
    from abjad.tools import mathtools

    # check input
    assert mathtools.is_positive_integer_equivalent_number(n)
    assert mathtools.is_positive_integer_equivalent_number(m)
    n, m = int(n), int(m)

    # initialize values
    result = []
    current_value = n
    double_m = 2 * m

    # partition n
    while double_m <= current_value:
        result.append(m)
        current_value -= m
    result.append(current_value)

    # return result
    return tuple(result)
