# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def all_are_assignable_integers(expr):
    '''True when `expr` is a sequence and all elements in `expr` are notehead-assignable integers:

    ::

        >>> sequencetools.all_are_assignable_integers([1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16])
        True

    True when `expr` is an empty sequence:

    ::

        >>> sequencetools.all_are_assignable_integers([])
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_assignable_integers('foo')
        False

    Returns boolean.
    '''

    try:
        return all(mathtools.is_assignable_integer(x) for x in expr)
    except TypeError:
        return False
