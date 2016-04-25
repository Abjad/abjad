# -*- coding: utf-8 -*-
import numbers


def is_positive_integer(expr):
    '''Is true when `expr` equals a positive integer.

    ::

        >>> mathtools.is_positive_integer(99)
        True

    Otherwise false:

    ::

        >>> mathtools.is_positive_integer(0)
        False

    ::

        >>> mathtools.is_positive_integer(-1)
        False

    Returns true or false.
    '''

    if isinstance(expr, numbers.Number):
        if expr == int(expr):
            if 0 < expr:
                return True

    return False
