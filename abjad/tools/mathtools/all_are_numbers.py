# -*- coding: utf-8 -*-
import numbers


def all_are_numbers(expr):
    '''Is true when `expr` is a sequence and all elements in `expr`
    are numbers:

    ::

        >>> mathtools.all_are_numbers([1, 2, 3.0, Fraction(13, 8)])
        True

    Is true when `expr` is an empty sequence:

    ::

        >>> mathtools.all_are_numbers([])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_numbers(17)
        False

    Returns true or false.
    '''

    try:
        return all(isinstance(x, numbers.Number) for x in expr)
    except TypeError:
        return False
