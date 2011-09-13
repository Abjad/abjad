from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex


def chromatic_pitch_name_to_diatonic_pitch_name(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_name` to diatonic pitch name::

        abjad> pitchtools.chromatic_pitch_name_to_diatonic_pitch_name("cs''")
        "c''"

    Return string.
    '''


    match = chromatic_pitch_name_regex.match(chromatic_pitch_name)

    if match is None:
        raise ValueError('\n\tNot chromatic pitch name: "%s".' % chromatic_pitch_name)

    groups = match.groups()
    diatonic_pitch_class_name, alphabetic_accidental_abbreviation, octave_tick_string = groups
    diatonic_pitch_name = diatonic_pitch_class_name + octave_tick_string

    return diatonic_pitch_name
