# -*- coding: utf-8 -*-


def is_positive_integer_equivalent_number(expr):
    '''Is true when `expr` is a positive integer-equivalent number.
    Otherwise false:

    ::

        >>> mathtools.is_positive_integer_equivalent_number(Duration(4, 2))
        True

    Returns true or false.
    '''
    from abjad.tools import mathtools

    try:
        return 0 < expr and mathtools.is_integer_equivalent_number(expr)
    except TypeError:  # Python 3 comparisons with non-numbers
        return False
