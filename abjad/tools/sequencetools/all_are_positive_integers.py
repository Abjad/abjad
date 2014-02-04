# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def all_are_positive_integers(expr):
    '''Is true when `expr` is a sequence and all elements  in `expr` 
    are positive integers.

    ::

        >>> sequencetools.all_are_positive_integers([1, 2, 3, 99])
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_positive_integers(17)
        False

    Returns boolean.
    '''

    try:
        return all(mathtools.is_positive_integer(x) for x in expr)
    except TypeError:
        return False
