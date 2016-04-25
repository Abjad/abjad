# -*- coding: utf-8 -*-


def all_are_positive_integers(expr):
    '''Is true when `expr` is a sequence and all elements  in `expr`
    are positive integers.

    ::

        >>> mathtools.all_are_positive_integers([1, 2, 3, 99])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_positive_integers(17)
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    try:
        return all(mathtools.is_positive_integer(x) for x in expr)
    except TypeError:
        return False
