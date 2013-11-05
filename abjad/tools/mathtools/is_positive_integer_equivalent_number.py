# -*- encoding: utf-8 -*-


def is_positive_integer_equivalent_number(expr):
    '''True when `expr` is a positive integer-equivalent number. 
    Otherwise false:

    ::

        >>> mathtools.is_positive_integer_equivalent_number(Duration(4, 2))
        True

    Returns boolean.
    '''
    from abjad.tools import mathtools

    return 0 < expr and mathtools.is_integer_equivalent_number(expr)
