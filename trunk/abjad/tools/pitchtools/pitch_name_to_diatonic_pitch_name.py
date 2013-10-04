# -*- encoding: utf-8 -*-


def pitch_name_to_diatonic_pitch_name(pitch_name):
    '''Change `pitch_name` to diatonic pitch name:

    ::

        >>> pitchtools.pitch_name_to_diatonic_pitch_name("cs''")
        "c''"

    Return string.
    '''
    from abjad.tools.pitchtools.is_pitch_name import pitch_name_regex

    match = pitch_name_regex.match(pitch_name)

    if match is None:
        raise ValueError('\n\tNot chromatic pitch name: "%s".' % pitch_name)

    groups = match.groups()
    diatonic_pitch_class_name, alphabetic_accidental_abbreviation, octave_tick_string = groups
    diatonic_pitch_name = diatonic_pitch_class_name + octave_tick_string

    return diatonic_pitch_name
