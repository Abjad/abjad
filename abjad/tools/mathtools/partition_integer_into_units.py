# -*- coding: utf-8 -*-


def partition_integer_into_units(n):
    r'''Partitions integer `n` into units.

    ..  container:: example

        With positive integer:

        ::

            >>> mathtools.partition_integer_into_units(6)
            [1, 1, 1, 1, 1, 1]

    ..  container:: example

        With negative integer:

        ::

            >>> mathtools.partition_integer_into_units(-5)
            [-1, -1, -1, -1, -1]

    ..  container:: example

        With zero:

        ::

            >>> mathtools.partition_integer_into_units(0)
            []

    Returns list of zero or more parts with absolute value equal to 1.
    '''
    from abjad.tools import mathtools
    result = abs(n) * [mathtools.sign(n) * 1]
    return result
