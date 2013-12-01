# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def all_are_nonnegative_integer_powers_of_two(expr):
    '''True when `expr` is a sequence and all elements in `expr`
    are nonnegative integer powers of two:

    ::

        >>> sequencetools.all_are_nonnegative_integer_powers_of_two([0, 1, 1, 1, 2, 4, 32, 32])
        True

    True when `expr` is an empty sequence:

    ::

        >>> sequencetools.all_are_nonnegative_integer_powers_of_two([])
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_nonnegative_integer_powers_of_two(17)
        False

    Returns boolean.
    '''

    try:
        return all(mathtools.is_nonnegative_integer_power_of_two(x) for x in expr)
    except TypeError:
        return False
