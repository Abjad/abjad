def apply_accidental_to_named_chromatic_pitch(named_chromatic_pitch, accidental = None):
    '''.. versionadded:: 2.0

    Apply `accidental` to `named_chromatic_pitch`::

        abjad> pitch = pitchtools.NamedChromaticPitch("cs''")
        abjad> pitchtools.apply_accidental_to_named_chromatic_pitch(pitch, 'f')
        NamedChromaticPitch("c''")

    Return new named pitch.
    '''

    from abjad.tools.pitchtools.Accidental import Accidental
    accidental = Accidental(accidental)
    new_accidental = named_chromatic_pitch._accidental + accidental
    new_name = named_chromatic_pitch.named_diatonic_pitch_class._diatonic_pitch_class_name + \
        new_accidental.alphabetic_accidental_abbreviation
    return type(named_chromatic_pitch)(new_name, named_chromatic_pitch.octave_number)
