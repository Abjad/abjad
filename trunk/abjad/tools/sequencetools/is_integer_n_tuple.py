def is_integer_n_tuple(expr, n):
    r'''.. versionadded:: 2.9

    True when `expr` is an integer tuple of length `n`::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_integer_n_tuple((19, 20, 21), 3)
        True

    Otherwise false::

        >>> sequencetools.is_integer_n_tuple((19, 20, 'text'), 3)
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == n and all([isinstance(x, int) for x in expr])
