def is_pair(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is a tuple of length ``2``::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_pair((19, 20))
        True

    Otherwise false::

        >>> sequencetools.is_pair((19, 20, 21))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 2
