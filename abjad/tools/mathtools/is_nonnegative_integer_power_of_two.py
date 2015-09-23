# -*- coding: utf-8 -*-
import fractions


def is_nonnegative_integer_power_of_two(expr):
    r'''Is true when `expr` is a nonnegative integer power of ``2``.

    ::

        >>> for n in range(10):
        ...     print(n, mathtools.is_nonnegative_integer_power_of_two(n))
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

    Returns true or false.
    '''

    if isinstance(expr, int):
        return not bool(expr & (expr - 1))
    elif isinstance(expr, fractions.Fraction):
        return is_nonnegative_integer_power_of_two(expr.numerator * expr.denominator)
    else:
        return False
