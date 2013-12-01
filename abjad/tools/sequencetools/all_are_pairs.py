# -*- encoding: utf-8 -*-


def all_are_pairs(expr):
    r'''True when `expr` is a sequence whose members are all sequences of length 2:

    ::

        >>> sequencetools.all_are_pairs([(1, 2), (3, 4), (5, 6), (7, 8)])
        True

    True when `expr` is an empty sequence:

    ::

        >>> sequencetools.all_are_pairs([])
        True

    Otherwise false:

    ::

        >>> sequencetools.all_are_pairs('foo')
        False

    Returns boolean.
    '''

    try:
        return all(len(x) == 2 for x in expr)
    except TypeError:
        return False
