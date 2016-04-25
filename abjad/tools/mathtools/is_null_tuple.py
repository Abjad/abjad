# -*- coding: utf-8 -*-


def is_null_tuple(expr):
    r'''Is true when `expr` is a tuple of length ``0``.

    ::

        >>> mathtools.is_null_tuple(())
        True

    Otherwise false:

    ::

        >>> mathtools.is_null_tuple((19, 20, 21))
        False

    Returns true or false.
    '''

    return isinstance(expr, tuple) and not len(expr)
