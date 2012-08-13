def sort_named_chromatic_pitch_carriers_in_expr(pitch_carriers):
    '''.. versionadded:: 2.0

    List named chromatic pitch carriers in `expr` sorted by numbered chromatic pitch-class::

        >>> chord = Chord([9, 11, 12, 14, 16], (1, 4))
        >>> notes = chordtools.arpeggiate_chord(chord)

    ::

        >>> pitchtools.sort_named_chromatic_pitch_carriers_in_expr(notes)
        [Note("c''4"), Note("d''4"), Note("e''4"), Note("a'4"), Note("b'4")]

    The elements in `pitch_carriers` are not changed in any way.

    Return list.
    '''
    from abjad.tools import pitchtools

    result = list(pitch_carriers[:])
    result.sort(lambda x, y: cmp(
            abs(pitchtools.list_named_chromatic_pitches_in_expr(x)[0].numbered_chromatic_pitch_class),
            abs(pitchtools.list_named_chromatic_pitches_in_expr(y)[0].numbered_chromatic_pitch_class)))

    return result
