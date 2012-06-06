def is_monotonically_decreasing_sequence(expr):
    r'''.. versionadded:: 2.0

    True when `expr` is a sequence and the elements in `expr` decrease monotonically::

        >>> from abjad.tools import sequencetools

    ::

        >>> expr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        >>> sequencetools.is_monotonically_decreasing_sequence(expr)
        True

    ::

        >>> expr = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
        >>> sequencetools.is_monotonically_decreasing_sequence(expr)
        True

    ::

        >>> expr = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        >>> sequencetools.is_monotonically_decreasing_sequence(expr)
        True

    False when `expr` is a sequence and the elements in `expr` do not decrease monotonically::

        >>> expr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> sequencetools.is_monotonically_decreasing_sequence(expr)
        False

    ::

        >>> expr = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
        >>> sequencetools.is_monotonically_decreasing_sequence(expr)
        False

    True when `expr` is a sequence and `expr` is empty::

        >>> expr = []
        >>> sequencetools.is_monotonically_decreasing_sequence(expr)
        True

    False when `expr` is not a sequence::

        >>> sequencetools.is_monotonically_decreasing_sequence(17)
        False

    Return boolean.
    '''

    try:
        prev = None
        for cur in expr:
            if prev is not None:
                if not cur <= prev:
                    return False
            prev = cur
        return True

    except TypeError:
        return False
