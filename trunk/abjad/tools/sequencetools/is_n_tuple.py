def is_n_tuple(expr, n):
    r'''.. versionadded 2.9

    True when `expr` is a tuple of length `n`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.is_n_tuple((19, 20, 21), 3)
        True

    Otherwise false::

        abjad> sequencetools.is_n_tuple((19, 20, 21), 4)
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == n
