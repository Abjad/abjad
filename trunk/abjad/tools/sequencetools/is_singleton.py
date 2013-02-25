def is_singleton(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is a tuple of length ``1``::

        >>> sequencetools.is_singleton((19,))
        True

    Otherwise false::

        >>> sequencetools.is_singleton((19, 20, 21))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 1
