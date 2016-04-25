# -*- coding: utf-8 -*-


def all_are_unequal(expr):
    '''Is true when `expr` is a sequence all elements in `expr` are unequal.

    ::

        >>> mathtools.all_are_unequal([1, 2, 3, 4, 9])
        True

    Is true when `expr` is an empty sequence:

    ::

        >>> mathtools.all_are_unequal([])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_unequal(17)
        False

    Returns true or false.
    '''

    try:
        return expr == type(expr)(set(expr))
    except TypeError:
        return False
