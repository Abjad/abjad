from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex


def chromatic_pitch_name_to_chromatic_pitch_class_name(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_name` to chromatic pitch-class name::

        abjad> pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name("cs''")
        'cs'

    Return string.
    '''

    match = chromatic_pitch_name_regex.match(chromatic_pitch_name)

    if match is None:
        raise ValueError('\n\tNot a chromatic pitch name: "%s".' % chromatic_pitch_name)

    groups = match.groups()
    diatonic_pitch_class_name, alphabetic_accidental_abbreviation, octave_tick_string = groups
    chromatic_pitch_class_name = diatonic_pitch_class_name + alphabetic_accidental_abbreviation

    return chromatic_pitch_class_name
