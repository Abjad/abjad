def is_integer_pair(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is an integer tuple of length ``2``::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_integer_pair((19, 20))
        True

    Otherwise false::

        >>> sequencetools.is_integer_pair(('some', 'text'))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 2 and all([isinstance(x, int) for x in expr])
