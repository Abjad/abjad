# -*- encoding: utf-8 -*-


def apply_accidental_to_named_pitch(named_pitch, accidental=None):
    '''Apply `accidental` to `named_pitch`:

    ::

        >>> pitch = pitchtools.NamedPitch("cs''")
        >>> pitchtools.apply_accidental_to_named_pitch(pitch, 'f')
        NamedPitch("c''")

    Return new named pitch.
    '''
    from abjad.tools import pitchtools

    accidental = pitchtools.Accidental(accidental)
    new_accidental = named_pitch._accidental + accidental
    new_name = pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name(
            named_pitch.chromatic_pitch_name)
    new_name += new_accidental.alphabetic_accidental_abbreviation
    #new_name = named_pitch.named_diatonic_pitch_class._diatonic_pitch_class_name + \
    #    new_accidental.alphabetic_accidental_abbreviation
    return type(named_pitch)(new_name, named_pitch.octave_number)
