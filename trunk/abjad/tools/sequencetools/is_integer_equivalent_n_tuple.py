# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def is_integer_equivalent_n_tuple(expr, n):
    r'''True when `expr` is a tuple of `n` integer-equivalent expressions:

    ::

        >>> sequencetools.is_integer_equivalent_n_tuple((2.0, '3', Fraction(4, 1)), 3)
        True

    Otherwise false:

    ::

        >>> sequencetools.is_integer_equivalent_n_tuple((2.5, '3', Fraction(4, 1)), 3)
        False

    Returns boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == n and \
        all(mathtools.is_integer_equivalent_expr(x) for x in expr)
