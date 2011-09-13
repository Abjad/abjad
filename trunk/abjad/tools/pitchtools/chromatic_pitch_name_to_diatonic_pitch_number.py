from abjad.tools.pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number import diatonic_pitch_class_name_to_diatonic_pitch_class_number
from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex
from abjad.tools.pitchtools.octave_tick_string_to_octave_number import octave_tick_string_to_octave_number


def chromatic_pitch_name_to_diatonic_pitch_number(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_name` to diatonic pitch number::

        abjad> pitchtools.chromatic_pitch_name_to_diatonic_pitch_number("cs''")
        7

    Return integer.
    '''

    if not isinstance(chromatic_pitch_name, str):
        raise TypeError

    match = chromatic_pitch_name_regex.match(chromatic_pitch_name)
    if match is None:
        raise ValueError

    groups = match.groups()
    diatonic_pitch_class_name, alphabetic_accidental_abbreviation, octave_tick_string = groups
    tmp = diatonic_pitch_class_name_to_diatonic_pitch_class_number
    diatonic_pitch_class_number = tmp(diatonic_pitch_class_name)
    octave_number = octave_tick_string_to_octave_number(octave_tick_string)
    diatonic_pitch_number = 7 * (octave_number - 4) + diatonic_pitch_class_number

    return diatonic_pitch_number
