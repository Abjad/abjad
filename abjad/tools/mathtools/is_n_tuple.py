# -*- coding: utf-8 -*-


def is_n_tuple(expr, n):
    r'''Is true when `expr` is a tuple of length `n`.

    ::

        >>> mathtools.is_n_tuple((19, 20, 21), 3)
        True

    Otherwise false:

    ::

        >>> mathtools.is_n_tuple((19, 20, 21), 4)
        False

    Returns true or false.
    '''

    return isinstance(expr, tuple) and len(expr) == n
