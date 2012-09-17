def permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row(pitches, row):
    '''.. versionadded:: 2.0

    Permute named chromatic pitch carrier list by twelve-tone `row`::

        >>> notes = notetools.make_notes([17, -10, -2, 11], [Duration(1, 4)])
        >>> row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
        >>> pitchtools.permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row(notes, row)
        [Note('bf4'), Note('d4'), Note("f''4"), Note("b'4")]

    Function works by reference only. No objects are copied.

    Return list.
    '''
    from abjad.tools import pitchtools
    from abjad.tools import notetools

    if not isinstance(row, pitchtools.TwelveToneRow):
        raise TypeError('must be twelve-tone row.')

    result = []

    for pc in row:
        matching_pitches = []
        for pitch in pitches:
            if isinstance(pitch, pitchtools.NamedChromaticPitch):
                if pitch.numbered_chromatic_pitch_class == pc:
                    matching_pitches.append(pitch)
            elif isinstance(pitch, notetools.Note):
                if pitch.written_pitch.numbered_chromatic_pitch_class == pc:
                    matching_pitches.append(pitch)
            else:
                raise TypeError('must be Abjad Pitch or Note.')
        result.extend(matching_pitches)

    return result
