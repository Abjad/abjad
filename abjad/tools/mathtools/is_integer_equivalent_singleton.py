# -*- coding: utf-8 -*-


def is_integer_equivalent_singleton(expr):
    r'''Is true when `expr` is a singleton of integer-equivalent expressions.

    ::

        >>> mathtools.is_integer_equivalent_singleton((2.0,))
        True

    Otherwise false:

    ::

        >>> mathtools.is_integer_equivalent_singleton((2.5,))
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    return isinstance(expr, tuple) and len(expr) == 1 and \
        all(mathtools.is_integer_equivalent_expr(x) for x in expr)
