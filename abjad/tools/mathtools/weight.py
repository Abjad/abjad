# -*- coding: utf-8 -*-


def weight(sequence):
    r'''Sum of the absolute value of the elements in `sequence`:

    ::

        >>> mathtools.weight([-1, -2, 3, 4, 5])
        15

    Returns nonnegative integer.
    '''

    return sum([abs(element) for element in sequence])
