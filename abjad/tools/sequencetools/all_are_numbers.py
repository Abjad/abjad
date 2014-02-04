# -*- encoding: utf-8 -*-
import numbers


def all_are_numbers(expr):
    '''Is true when `expr` is a sequence and all elements in `expr` 
    are numbers:

    ::

        >>> sequencetools.all_are_numbers([1, 2, 3.0, Fraction(13, 8)])
        True

    Is true when `expr` is an empty sequence:

    ::

        >>> sequencetools.all_are_numbers([])
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_numbers(17)
        False

    Returns boolean.
    '''

    try:
        return all(isinstance(x, numbers.Number) for x in expr)
    except TypeError:
        return False
