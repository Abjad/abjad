import numbers


# TODO: make public?
def _transpose_pitch_carrier_by_melodic_chromatic_interval(
    pitch_carrier, melodic_chromatic_interval):
    '''.. versionadded:: 2.0

    Transpose `pitch_carrier` by `melodic_chromatic_interval`:

    ::

        >>> from abjad.tools.pitchtools._transpose_pitch_carrier_by_melodic_chromatic_interval import _transpose_pitch_carrier_by_melodic_chromatic_interval
        >>> pitch = pitchtools.NamedChromaticPitch(12)
        >>> mci = pitchtools.MelodicChromaticInterval(-3)
        >>> _transpose_pitch_carrier_by_melodic_chromatic_interval(pitch, mci)
        NamedChromaticPitch("a'")

    Return new `pitch_carrier` object.
    '''
    from abjad.tools import chordtools
    from abjad.tools import componenttools
    from abjad.tools import notetools
    from abjad.tools import pitchtools

    mci = pitchtools.MelodicChromaticInterval(melodic_chromatic_interval)
    if isinstance(pitch_carrier, pitchtools.Pitch):
        number = pitch_carrier.chromatic_pitch_number + mci.semitones
        return type(pitch_carrier)(number)
    elif isinstance(pitch_carrier, numbers.Number):
        pitch_carrier = pitchtools.NumberedChromaticPitch(pitch_carrier)
        result = _transpose_pitch_carrier_by_melodic_chromatic_interval(
            pitch_carrier, mci)
        return result.chromatic_pitch_number
    elif isinstance(pitch_carrier, notetools.Note):
        new_note = componenttools.copy_components_and_remove_spanners(
            [pitch_carrier])[0]
        number = abs(pitch_carrier.written_pitch.numbered_chromatic_pitch)
        number += mci.number
        new_pitch = pitchtools.NamedChromaticPitch(number)
        new_note.written_pitch = new_pitch
        return new_note
    elif isinstance(pitch_carrier, chordtools.Chord):
        new_chord = componenttools.copy_components_and_remove_spanners(
            [pitch_carrier])[0]
        for new_nh, old_nh in \
            zip(new_chord.note_heads, pitch_carrier.note_heads):
            number = abs(old_nh.written_pitch.numbered_chromatic_pitch)
            number += mci.number
            new_pitch = pitchtools.NamedChromaticPitch(number)
            new_nh.written_pitch = new_pitch
        return new_chord
    else:
        return pitch_carrier
