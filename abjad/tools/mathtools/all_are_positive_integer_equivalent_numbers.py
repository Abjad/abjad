# -*- coding: utf-8 -*-


def all_are_positive_integer_equivalent_numbers(expr):
    '''Is true when `expr` is a sequence and all elements in `expr` are
    positive integer-equivalent numbers. Otherwise false:

    ::

        >>> mathtools.all_are_positive_integer_equivalent_numbers([Fraction(4, 2), 2.0, 2])
        True

    Returns true or false.
    '''
    from abjad.tools import mathtools

    try:
        return all(mathtools.is_positive_integer_equivalent_number(x) for x in expr)
    except TypeError:
        return False
