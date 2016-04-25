# -*- coding: utf-8 -*-
import numbers


def is_integer_equivalent_expr(expr):
    '''Is true when `expr` is an integer-equivalent number.

    ::

        >>> mathtools.is_integer_equivalent_expr(12.0)
        True

    Is true when `expr` evaluates to an integer:

    ::

        >>> mathtools.is_integer_equivalent_expr('12')
        True

    Otherwise false:

    ::

        >>> mathtools.is_integer_equivalent_expr('foo')
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    if isinstance(expr, numbers.Number):
        return mathtools.is_integer_equivalent_number(expr)

    try:
        int(expr)
        return True
    except (TypeError, ValueError):
        return False
