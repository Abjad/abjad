# -*- coding: utf-8 -*-


def is_pair(expr):
    r'''Is true when `expr` is a tuple of length ``2``.

    ::

        >>> mathtools.is_pair((19, 20))
        True

    Otherwise false:

    ::

        >>> mathtools.is_pair((19, 20, 21))
        False

    Returns true or false.
    '''

    return isinstance(expr, tuple) and len(expr) == 2
