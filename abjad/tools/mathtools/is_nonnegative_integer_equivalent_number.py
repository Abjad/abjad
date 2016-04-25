# -*- coding: utf-8 -*-


def is_nonnegative_integer_equivalent_number(expr):
    '''Is true when `expr` is a nonnegative integer-equivalent number.
    Otherwise false:

    ::

        >>> mathtools.is_nonnegative_integer_equivalent_number(Duration(4, 2))
        True

    Returns true or false.
    '''
    from abjad.tools import mathtools

    return mathtools.is_integer_equivalent_number(expr) and 0 <= expr
