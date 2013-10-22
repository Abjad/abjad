# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def is_integer_equivalent_singleton(expr):
    r'''True when `expr` is a singleton of integer-equivalent expressions:

    ::

        >>> sequencetools.is_integer_equivalent_singleton((2.0,))
        True

    Otherwise false:

    ::

        >>> sequencetools.is_integer_equivalent_singleton((2.5,))
        False

    Returns boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 1 and \
        all(mathtools.is_integer_equivalent_expr(x) for x in expr)
