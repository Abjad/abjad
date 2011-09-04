def is_monotonically_increasing_sequence(expr):
    r'''.. versionadded:: 2.0

    True when `expr` is a sequence and the elements in `expr` increase monotonically::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> expr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        abjad> sequencetools.is_monotonically_increasing_sequence(expr)
        True

    ::

        abjad> expr = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
        abjad> sequencetools.is_monotonically_increasing_sequence(expr)
        True

    ::

        abjad> expr = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        abjad> sequencetools.is_monotonically_increasing_sequence(expr)
        True

    False when `expr` is a sequence and the elements in `expr` do not increase monotonically::

        abjad> expr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        abjad> sequencetools.is_monotonically_increasing_sequence(expr)
        False

    ::

        abjad> expr = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
        abjad> sequencetools.is_monotonically_increasing_sequence(expr)
        False

    True when `expr` is a sequence and `expr` is empty::

        abjad> expr = []
        abjad> sequencetools.is_monotonically_increasing_sequence(expr)
        True

    False when `expr` is not a sequence::

        abjad> sequencetools.is_monotonically_increasing_sequence(17)
        False

    Return boolean.
    '''

    try:
        prev = None
        for cur in expr:
            if prev is not None:
                if not prev <= cur:
                    return False
            prev = cur
        return True

    except TypeError:
        return False
