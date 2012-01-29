from abjad.tools.mathtools.is_integer_equivalent_number import is_integer_equivalent_number
from numbers import Number


def is_integer_equivalent_expr(expr):
    '''.. versionadded:: 2.5

    True when `expr` is an integer-equivalent number::


        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.is_integer_equivalent_expr(12.0)
        True

    True when `expr` evaluates to an integer::

        abjad> mathtools.is_integer_equivalent_expr('12')
        True

    Otherwise false::

        abjad> mathtools.is_integer_equivalent_expr('foo')
        False

    Return boolean.
    '''

    if isinstance(expr, Number):
        return is_integer_equivalent_number(expr)

    try:
        int(expr)
        return True
    except (TypeError, ValueError):
        return False
