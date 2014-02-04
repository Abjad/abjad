# -*- encoding: utf-8 -*-


def is_integer_pair(expr):
    r'''Is true when `expr` is an integer tuple of length ``2``.

    ::

        >>> sequencetools.is_integer_pair((19, 20))
        True

    Otherwise false:

    ::

        >>> sequencetools.is_integer_pair(('some', 'text'))
        False

    Returns boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 2 and \
        all(isinstance(x, int) for x in expr)
