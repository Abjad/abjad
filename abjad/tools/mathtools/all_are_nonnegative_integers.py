# -*- coding: utf-8 -*-


def all_are_nonnegative_integers(expr):
    '''Is true when `expr` is a sequence and all elements  in `expr`
    are nonnegative integers.

    ::

        >>> mathtools.all_are_nonnegative_integers([0, 1, 2, 99])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_nonnegative_integers([0, 1, 2, -99])
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    try:
        return all(mathtools.is_nonnegative_integer(x) for x in expr)
    except TypeError:
        return False
