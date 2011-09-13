from abjad.tools.pitchtools.is_diatonic_pitch_name import diatonic_pitch_name_regex


def diatonic_pitch_name_to_diatonic_pitch_class_name(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to diatonic pitch-class name::

        abjad> pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_name("c''")
        'c'

    Return string.
    '''

    match = diatonic_pitch_name_regex.match(diatonic_pitch_name)

    if match is None:
        raise ValueError('\n\tNot a diatonic pitch name: "%s".' % diatonic_pitch_name)

    diatonic_pitch_class_name, octave_tick_string = match.groups()

    return diatonic_pitch_class_name
