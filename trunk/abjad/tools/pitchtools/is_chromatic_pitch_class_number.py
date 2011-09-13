def is_chromatic_pitch_class_number(expr):
    '''.. versionadded:: 2.0

    True `expr` is a chromatic pitch-class number. Otherwise false::

        abjad> pitchtools.is_chromatic_pitch_class_number(1)
        True

    The chromatic pitch-class numbers are equal to the set ``[0, 0.5, ..., 11, 11.5]``.

    Return boolean.
    '''

    return expr in [(n).__truediv__(2) for n in range(24)]
