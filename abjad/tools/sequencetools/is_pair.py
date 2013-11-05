# -*- encoding: utf-8 -*-


def is_pair(expr):
    r'''True when `expr` is a tuple of length ``2``:

    ::

        >>> sequencetools.is_pair((19, 20))
        True

    Otherwise false:

    ::

        >>> sequencetools.is_pair((19, 20, 21))
        False

    Returns boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 2
