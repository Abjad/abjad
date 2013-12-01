# -*- encoding: utf-8 -*-


def all_are_unequal(expr):
    '''True when `expr` is a sequence all elements in `expr` are unequal:

    ::

        >>> sequencetools.all_are_unequal([1, 2, 3, 4, 9])
        True

    True when `expr` is an empty sequence:

    ::

        >>> sequencetools.all_are_unequal([])
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_unequal(17)
        False

    Returns boolean.
    '''

    try:
        return expr == type(expr)(set(expr))
    except TypeError:
        return False
