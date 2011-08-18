from fractions import Fraction


def is_nonnegative_integer_power_of_two(expr):
    '''True when `expr` is a nonnegative integer power of ``2``::

        abjad> from abjad.tools import mathtools

    ::

        abjad> for n in range(10):
        ...     print n, mathtools.is_nonnegative_integer_power_of_two(n)
        ...
        0 True
        1 True
        2 True
        3 False
        4 True
        5 False
        6 False
        7 False
        8 True
        9 False

    Otherwise false.

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``mathtools.is_power_of_two()`` to
        ``mathtools.is_nonnegative_integer_power_of_two()``.
    '''

    if isinstance(expr, (int, long)):
        return not bool(expr & (expr - 1))
    elif isinstance(expr, Fraction):
        return is_nonnegative_integer_power_of_two(expr.numerator * expr.denominator)
    else:
        return False
