# -*- coding: utf-8 -*-


def is_integer_singleton(expr):
    r'''Is true when `expr` is an integer tuple of of length ``1``.

    ::

        >>> mathtools.is_integer_singleton((19,))
        True

    Otherwise false:

    ::

        >>> mathtools.is_integer_singleton(('text',))
        False

    Returns true or false.
    '''

    return isinstance(expr, tuple) and \
        len(expr) == 1 and \
        isinstance(expr[0], int)
