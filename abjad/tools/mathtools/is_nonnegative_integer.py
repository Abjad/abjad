# -*- coding: utf-8 -*-
import numbers


def is_nonnegative_integer(expr):
    '''Is true when `expr` equals a nonnegative integer.

    ::

        >>> mathtools.is_nonnegative_integer(99)
        True

    ::

        >>> mathtools.is_nonnegative_integer(0)
        True

    Otherwise false:

    ::

        >>> mathtools.is_nonnegative_integer(-1)
        False

    Returns true or false.
    '''

    if isinstance(expr, numbers.Number):
        if expr == int(expr):
            if 0 <= expr:
                return True

    return False
