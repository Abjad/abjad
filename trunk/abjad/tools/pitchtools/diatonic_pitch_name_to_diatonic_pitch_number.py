# -*- encoding: utf-8 -*-


def diatonic_pitch_name_to_diatonic_pitch_number(diatonic_pitch_name):
    '''Change `diatonic_pitch_name` to diatonic pitch number:

    ::

        >>> pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("c''")
        7

    Return integer.
    '''
    from abjad.tools import pitchtools

    match = pitchtools.Pitch._diatonic_pitch_name_regex.match(
        diatonic_pitch_name)
    if match is None:
        raise TypeError

    diatonic_pitch_class_name, octave_tick_string = match.groups()
    tmp = pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number
    diatonic_pitch_class_number = tmp(diatonic_pitch_class_name)
    octave_number = \
        pitchtools.OctaveIndication(octave_tick_string).octave_number
    diatonic_pitch_number = 7 * (octave_number - 4) + diatonic_pitch_class_number

    return diatonic_pitch_number
