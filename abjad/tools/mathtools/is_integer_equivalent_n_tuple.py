# -*- coding: utf-8 -*-


def is_integer_equivalent_n_tuple(expr, n):
    r'''Is true when `expr` is a tuple of `n` integer-equivalent expressions.

    ::

        >>> mathtools.is_integer_equivalent_n_tuple((2.0, '3', Fraction(4, 1)), 3)
        True

    Otherwise false:

    ::

        >>> mathtools.is_integer_equivalent_n_tuple((2.5, '3', Fraction(4, 1)), 3)
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    return isinstance(expr, tuple) and len(expr) == n and \
        all(mathtools.is_integer_equivalent_expr(x) for x in expr)
