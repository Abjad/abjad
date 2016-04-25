# -*- coding: utf-8 -*-


def all_are_nonnegative_integer_powers_of_two(expr):
    '''Is true when `expr` is a sequence and all elements in `expr`
    are nonnegative integer powers of two.

    ::

        >>> mathtools.all_are_nonnegative_integer_powers_of_two([0, 1, 1, 1, 2, 4, 32, 32])
        True

    Is true when `expr` is an empty sequence:

    ::

        >>> mathtools.all_are_nonnegative_integer_powers_of_two([])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_nonnegative_integer_powers_of_two(17)
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    try:
        return all(
            mathtools.is_nonnegative_integer_power_of_two(x) for x in expr
            )
    except TypeError:
        return False
