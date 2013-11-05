# -*- encoding: utf-8 -*-


def is_integer_singleton(expr):
    r'''True when `expr` is an integer tuple of of length ``1``:

    ::

        >>> sequencetools.is_integer_singleton((19,))
        True

    Otherwise false:

    ::

        >>> sequencetools.is_integer_singleton(('text',))
        False

    Returns boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 1 and isinstance(expr[0], int)
