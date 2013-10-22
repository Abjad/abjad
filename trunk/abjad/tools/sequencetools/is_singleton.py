# -*- encoding: utf-8 -*-


def is_singleton(expr):
    r'''True when `expr` is a tuple of length ``1``:

    ::

        >>> sequencetools.is_singleton((19,))
        True

    Otherwise false:

    ::

        >>> sequencetools.is_singleton((19, 20, 21))
        False

    Returns boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 1
