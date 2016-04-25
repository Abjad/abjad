# -*- coding: utf-8 -*-


def is_fraction_equivalent_pair(expr):
    r'''Is true when `expr` is an integer-equivalent pair of numbers
    excluding ``0`` as the second term.

    ::

        >>> mathtools.is_fraction_equivalent_pair((2, 3))
        True

    Otherwise false:

    ::

        >>> mathtools.is_fraction_equivalent_pair((2, 0))
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    return mathtools.is_integer_equivalent_pair(expr) and not expr[1] == 0
