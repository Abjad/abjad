# TODO: make public?
def _transpose_pitch_carrier_by_melodic_diatonic_interval(pitch_carrier, melodic_diatonic_interval):
    '''.. versionadded:: 2.0

    Transpose `pitch_carrier` by `melodic_diatonic_interval`::

        >>> from abjad.tools.pitchtools._transpose_pitch_carrier_by_melodic_diatonic_interval import _transpose_pitch_carrier_by_melodic_diatonic_interval

        >>> pitch_carrier = pitchtools.NamedChromaticPitch("c''")
        >>> mdi = pitchtools.MelodicDiatonicInterval('minor', -3)
        >>> _transpose_pitch_carrier_by_melodic_diatonic_interval(pitch_carrier, mdi)
        NamedChromaticPitch("a'")

    Return named chromatic pitch.
    '''
    from abjad.tools import chordtools
    from abjad.tools import componenttools
    from abjad.tools import notetools
    from abjad.tools import pitchtools

    # TODO: remove try / except block
    try:
        mdi = pitchtools.MelodicDiatonicInterval(melodic_diatonic_interval)
    except (TypeError, ValueError):
        raise TypeError('must be melodic diatonic interval.')

    if isinstance(pitch_carrier, pitchtools.PitchObject):
        return _transpose_pitch_by_melodic_diatonic_interval(pitch_carrier, mdi)
    elif isinstance(pitch_carrier, notetools.Note):
        new_note = componenttools.copy_components_and_remove_spanners([pitch_carrier])[0]
        new_pitch = _transpose_pitch_by_melodic_diatonic_interval(pitch_carrier.written_pitch, mdi)
        new_note.written_pitch = new_pitch
        return new_note
    elif isinstance(pitch_carrier, chordtools.Chord):
        new_chord = componenttools.copy_components_and_remove_spanners([pitch_carrier])[0]
        for new_nh, old_nh in zip(new_chord.note_heads, pitch_carrier.note_heads):
            new_pitch = _transpose_pitch_by_melodic_diatonic_interval(old_nh.written_pitch, mdi)
            new_nh.written_pitch = new_pitch
        return new_chord
    else:
        #raise TypeError('must be pitch, note or chord: %s' % str(pitch_carrier))
        return pitch_carrier


def _transpose_pitch_by_melodic_diatonic_interval(pitch, mdi):
    from abjad.tools import pitchtools

    chromatic_pitch_number = pitch.chromatic_pitch_number + mdi.semitones
    diatonic_pitch_class_number = (pitch.diatonic_pitch_class_number + mdi.staff_spaces) % 7
    diatonic_pitch_class_name = pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(
        diatonic_pitch_class_number)
    named_chromatic_pitch = pitchtools.NamedChromaticPitch(chromatic_pitch_number, diatonic_pitch_class_name)
    return type(pitch)(named_chromatic_pitch)
