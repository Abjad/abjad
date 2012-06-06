def is_null_tuple(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is a tuple of length ``0``::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_null_tuple(())
        True

    Otherwise false::

        >>> sequencetools.is_null_tuple((19, 20, 21))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and not len(expr)
