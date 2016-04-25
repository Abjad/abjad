# -*- coding: utf-8 -*-
import numbers


def is_negative_integer(expr):
    '''Is true when `expr` equals a negative integer.

    ::

        >>> mathtools.is_negative_integer(-1)
        True

    Otherwise false:

    ::

        >>> mathtools.is_negative_integer(0)
        False

    ::

        >>> mathtools.is_negative_integer(99)
        False

    Returns true or false.
    '''

    if isinstance(expr, numbers.Number):
        if expr == int(expr):
            if expr < 0:
                return True

    return False
