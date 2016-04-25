# -*- coding: utf-8 -*-


def all_are_pairs(expr):
    r'''Is true when `expr` is a sequence whose members are all sequences
    of length 2.

    ::

        >>> mathtools.all_are_pairs([(1, 2), (3, 4), (5, 6), (7, 8)])
        True

    Is true when `expr` is an empty sequence:

    ::

        >>> mathtools.all_are_pairs([])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_pairs('foo')
        False

    Returns true or false.
    '''

    try:
        return all(len(x) == 2 for x in expr)
    except TypeError:
        return False
