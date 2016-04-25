# -*- coding: utf-8 -*-


def all_are_integer_equivalent_numbers(expr):
    '''Is true when `expr` is a sequence and all elements in `expr`
    are integer-equivalent numbers.

    ::

        >>> mathtools.all_are_integer_equivalent_numbers([1, 2, 3.0, Fraction(4, 1)])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_integer_equivalent_numbers([1, 2, 3.5, 4])
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    try:
        return all(mathtools.is_integer_equivalent_number(x) for x in expr)
    except TypeError:
        return False
