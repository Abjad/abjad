from abjad.tools.pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number import diatonic_pitch_class_name_to_diatonic_pitch_class_number
from abjad.tools.pitchtools.is_diatonic_pitch_name import diatonic_pitch_name_regex
from abjad.tools.pitchtools.octave_tick_string_to_octave_number import octave_tick_string_to_octave_number


def diatonic_pitch_name_to_diatonic_pitch_number(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to diatonic pitch number::

        abjad> pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("c''")
        7

    Return integer.
    '''

    match = diatonic_pitch_name_regex.match(diatonic_pitch_name)
    if match is None:
        raise TypeError

    diatonic_pitch_class_name, octave_tick_string = match.groups()
    tmp = diatonic_pitch_class_name_to_diatonic_pitch_class_number
    diatonic_pitch_class_number = tmp(diatonic_pitch_class_name)
    octave_number = octave_tick_string_to_octave_number(octave_tick_string)
    diatonic_pitch_number = 7 * (octave_number - 4) + diatonic_pitch_class_number

    return diatonic_pitch_number
