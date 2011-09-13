from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def list_named_chromatic_pitch_carriers_in_expr_sorted_by_numbered_chromatic_pitch_class(
    pitch_carriers):
    '''.. versionadded:: 2.0

    List named chromatic pitch carriers in `expr` sorted by numbered chromatic pitch-class::

        abjad> chord = Chord([9, 11, 12, 14, 16], (1, 4))
        abjad> notes = chordtools.arpeggiate_chord(chord)
        abjad> pitchtools.list_named_chromatic_pitch_carriers_in_expr_sorted_by_numbered_chromatic_pitch_class(notes)
        [Note("c''4"), Note("d''4"), Note("e''4"), Note("a'4"), Note("b'4")]

    The elements in `pitch_carriers` are not changed in any way.

    Return list.

    .. versionchanged:: 2.0
        renamed ``pitchtools.list_named_chromatic_pitch_carriers_in_expr_sorted_by_numeric_chromatic_pitch_class()`` to
        ``pitchtools.list_named_chromatic_pitch_carriers_in_expr_sorted_by_numbered_chromatic_pitch_class()``.
    '''

    result = list(pitch_carriers[:])
    result.sort(lambda x, y: cmp(
            abs(list_named_chromatic_pitches_in_expr(x)[0].numbered_chromatic_pitch_class),
            abs(list_named_chromatic_pitches_in_expr(y)[0].numbered_chromatic_pitch_class)))

    return result
