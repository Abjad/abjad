def list_numbered_chromatic_pitch_classes_in_expr(expr):
    '''.. versionadded:: 2.0

    List numbered chromatic pitch-classes in `expr`::

        >>> chord = Chord("<cs'' d'' ef''>4")

    ::

        >>> for x in pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord):
        ...     x
        ...
        NumberedChromaticPitchClass(1)
        NumberedChromaticPitchClass(2)
        NumberedChromaticPitchClass(3)

    Works with notes, chords, defective chords.

    Return tuple or zero or more numbered chromatic pitch-classes.

    .. versionchanged:: 2.0
        renamed ``pitchtools.list_numeric_chromatic_pitch_classes_in_expr()`` to
        ``pitchtools.list_numbered_chromatic_pitch_classes_in_expr()``.
    '''
    from abjad.tools import pitchtools

    pitches = pitchtools.list_named_chromatic_pitches_in_expr(expr)
    pitch_classes = [pitchtools.NumberedChromaticPitchClass(pitch) for pitch in pitches]
    pitch_classes = tuple(pitch_classes)
    return pitch_classes
