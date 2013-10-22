# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def all_are_integer_equivalent_exprs(expr):
    '''True when `expr` is a sequence and all elements in `expr` are integer-equivalent expressions:

    ::

        >>> sequencetools.all_are_integer_equivalent_exprs([1, '2', 3.0, Fraction(4, 1)])
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_integer_equivalent_exprs([1, '2', 3.5, 4])
        False

    Returns boolean.
    '''

    try:
        return all(mathtools.is_integer_equivalent_expr(x) for x in expr)
    except TypeError:
        return False
