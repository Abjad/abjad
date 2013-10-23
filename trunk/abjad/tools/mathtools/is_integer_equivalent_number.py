# -*- encoding: utf-8 -*-
import numbers


def is_integer_equivalent_number(expr):
    '''True when `expr` is a number and `expr` is equivalent to an integer.

    ::

        >>> mathtools.is_integer_equivalent_number(12.0)
        True

    Otherwise false:

    ::

        >>> mathtools.is_integer_equivalent_number(Duration(1, 2))
        False

    Returns boolean.
    '''

    if isinstance(expr, numbers.Number):
        if int(expr) == expr:
            return True

    return False
