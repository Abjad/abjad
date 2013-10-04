# -*- encoding: utf-8 -*-


def pitch_name_to_diatonic_pitch_number(pitch_name):
    '''Change `pitch_name` to diatonic pitch number:

    ::

        >>> pitchtools.pitch_name_to_diatonic_pitch_number("cs''")
        7

    Return integer.
    '''
    from abjad.tools import pitchtools

    if not isinstance(pitch_name, str):
        raise TypeError

    match = pitchtools.Pitch._pitch_name_regex.match(pitch_name)
    if match is None:
        raise ValueError

    groups = match.groups()
    diatonic_pitch_class_name, alphabetic_accidental_abbreviation, octave_tick_string = groups
    tmp = pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number
    diatonic_pitch_class_number = tmp(diatonic_pitch_class_name)
    octave_number = \
        pitchtools.OctaveIndication(octave_tick_string).octave_number
    diatonic_pitch_number = 7 * (octave_number - 4) + diatonic_pitch_class_number

    return diatonic_pitch_number
