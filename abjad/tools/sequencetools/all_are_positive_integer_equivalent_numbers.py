# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def all_are_positive_integer_equivalent_numbers(expr):
    '''True when `expr` is a sequence and all elements in `expr` are positive
    integer-equivalent numbers. Otherwise false:

    ::

        >>> sequencetools.all_are_positive_integer_equivalent_numbers([Fraction(4, 2), 2.0, 2])
        True

    Returns boolean.
    '''

    try:
        return all(mathtools.is_positive_integer_equivalent_number(x) for x in expr)
    except TypeError:
        return False
