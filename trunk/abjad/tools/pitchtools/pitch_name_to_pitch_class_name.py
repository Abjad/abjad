# -*- encoding: utf-8 -*-


def pitch_name_to_pitch_class_name(pitch_name):
    '''Change `pitch_name` to chromatic pitch-class name:

    ::

        >>> pitchtools.pitch_name_to_pitch_class_name("cs''")
        'cs'

    Return string.
    '''
    from abjad.tools.pitchtools.is_pitch_name import pitch_name_regex

    match = pitch_name_regex.match(pitch_name)

    if match is None:
        raise ValueError('\n\tNot a chromatic pitch name: "%s".' % pitch_name)

    groups = match.groups()
    diatonic_pitch_class_name, alphabetic_accidental_abbreviation, octave_tick_string = groups
    pitch_class_name = diatonic_pitch_class_name + alphabetic_accidental_abbreviation

    return pitch_class_name
