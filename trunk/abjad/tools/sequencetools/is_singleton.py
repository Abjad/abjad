def is_singleton(expr):
    r'''.. versionadded:: 2.9
    
    True when `expr` is a tuple of length ``1``::

        >>> from abjad.tools import sequencetools
    
    ::

        >>> sequencetools.is_singleton((19,))
        True

    Otherwise false::

        abajd> sequencetools.is_singleton((19, 20, 21))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 1
