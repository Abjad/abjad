# -*- encoding: utf-8 -*-


def pitch_class_name_to_chromatic_pitch_class_number(pitch_class_name):
    '''Change `pitch_class_name` to chromatic pitch-class number:

    ::

        >>> pitchtools.pitch_class_name_to_chromatic_pitch_class_number('cs')
        1

    Return chromatic pitch-class number.
    '''
    from abjad.tools import pitchtools
    from abjad.tools.pitchtools.is_pitch_class_name import pitch_class_name_regex

    match = pitch_class_name_regex.match(pitch_class_name)
    if match is None:
        raise ValueError('\n\tNot chromatic pitch-class name: "%s".' % pitch_class_name)

    diatonic_pitch_class_name, alphabetic_accidental_abbreviation = match.groups()
    diatonic_pitch_class_number = pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number(
        diatonic_pitch_class_name)
    chromatic_pitch_class_number = pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(
        diatonic_pitch_class_number)
    accidental = pitchtools.Accidental(alphabetic_accidental_abbreviation)
    chromatic_pitch_class_number += accidental.semitones
    chromatic_pitch_class_number %= 12

    return chromatic_pitch_class_number
