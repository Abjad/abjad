# -*- encoding: utf-8 -*-


def is_n_tuple(expr, n):
    r'''Is true when `expr` is a tuple of length `n`:

    ::

        >>> sequencetools.is_n_tuple((19, 20, 21), 3)
        True

    Otherwise false:

    ::

        >>> sequencetools.is_n_tuple((19, 20, 21), 4)
        False

    Returns boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == n
