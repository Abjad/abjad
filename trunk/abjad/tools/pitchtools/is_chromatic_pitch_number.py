def is_chromatic_pitch_number(expr):
    '''.. versionadded:: 2.0

    True `expr` is a chromatic pitch number. Otherwise false::

        abjad> pitchtools.is_chromatic_pitch_number(13)
        True

    The chromatic pitch numbers are equal to the set of all integers in union
    with the set of all integers plus of minus ``0.5``.

    Return boolean.
    '''

    if isinstance(expr, (int, long, float)):
        return expr % 0.5 == 0
    return False
