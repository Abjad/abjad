# -*- encoding: utf-8 -*-


def is_permutation(expr, length=None):
    '''True when `expr` is a permutation:

    ::

        >>> sequencetools.is_permutation([4, 5, 0, 3, 2, 1])
        True

    Otherwise false:

    ::

        >>> sequencetools.is_permutation([1, 1, 5, 3, 2, 1])
        False

    True when `expr` is a permutation of first `length` nonnegative integers:

    ::

        >>> sequencetools.is_permutation([4, 5, 0, 3, 2, 1], length=6)
        True

    Otherwise false:

    ::

        >>> sequencetools.is_permutation([4, 0, 3, 2, 1], length=6)
        False

    Returns boolean.
    '''

    try:
        if length is None:
            length = len(expr)
        return sorted(expr) == range(length)
    except:
        return False
