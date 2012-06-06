def is_integer_singleton(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is an integer tuple of of length ``1``::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_integer_singleton((19,))
        True

    Otherwise false::

        >>> sequencetools.is_integer_singleton(('text',))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 1 and isinstance(expr[0], int)
