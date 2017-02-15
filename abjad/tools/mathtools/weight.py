# -*- coding: utf-8 -*-


def weight(argument):
    r'''Gets weight of `argument`.

    ..  container:: example

        ::

            >>> mathtools.weight([-1, -2, 3, 4, 5])
            15

    ..  container:: example

        ::

            >>> mathtools.weight([])
            0

    Defined equal to sum of the absolute value of items in `argument`.

    Returns nonnegative integer.
    '''
    return sum([abs(_) for _ in argument])
