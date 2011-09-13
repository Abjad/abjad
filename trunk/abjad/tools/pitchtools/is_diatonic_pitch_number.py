def is_diatonic_pitch_number(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a diatonic pitch number. Otherwise false::

        abjad> pitchtools.is_diatonic_pitch_number(7)
        True

    The diatonic pitch numbers are equal to the set of integers.

    Return boolean.
    '''

    return isinstance(expr, (int, long))
