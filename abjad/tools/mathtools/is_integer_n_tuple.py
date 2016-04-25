# -*- coding: utf-8 -*-


def is_integer_n_tuple(expr, n):
    r'''Is true when `expr` is an integer tuple of length `n`.

    ::

        >>> mathtools.is_integer_n_tuple((19, 20, 21), 3)
        True

    Otherwise false:

    ::

        >>> mathtools.is_integer_n_tuple((19, 20, 'text'), 3)
        False

    Returns true or false.
    '''

    return isinstance(expr, tuple) and len(expr) == n and \
        all(isinstance(x, int) for x in expr)
