# -*- coding: utf-8 -*-


def is_singleton(expr):
    r'''Is true when `expr` is a tuple of length ``1``.

    ::

        >>> mathtools.is_singleton((19,))
        True

    Otherwise false:

    ::

        >>> mathtools.is_singleton((19, 20, 21))
        False

    Returns true or false.
    '''

    return isinstance(expr, tuple) and len(expr) == 1
