# -*- coding: utf-8 -*-


def is_integer_equivalent_pair(expr):
    r'''Is true when `expr` is a pair of integer-equivalent expressions.

    ::

        >>> mathtools.is_integer_equivalent_pair((2.0, '3'))
        True

    Otherwise false:

    ::

        >>> mathtools.is_integer_equivalent_pair((2.5, '3'))
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    return isinstance(expr, tuple) and len(expr) == 2 and \
        all(mathtools.is_integer_equivalent_expr(x) for x in expr)
