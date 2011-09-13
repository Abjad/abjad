from abjad.tools.pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name import diatonic_pitch_class_number_to_diatonic_pitch_class_name
from abjad.tools.pitchtools.is_diatonic_pitch_number import is_diatonic_pitch_number
from abjad.tools.pitchtools.octave_number_to_octave_tick_string import octave_number_to_octave_tick_string


def diatonic_pitch_number_to_diatonic_pitch_name(diatonic_pitch_number):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_number` to diatonic pitch name::

        abjad> pitchtools.diatonic_pitch_number_to_diatonic_pitch_name(7)
        "c''"

    Return string.
    '''

    if not is_diatonic_pitch_number(diatonic_pitch_number):
        raise TypeError

    diatonic_pitch_class_number = diatonic_pitch_number % 7
    diatonic_pitch_class_name = diatonic_pitch_class_number_to_diatonic_pitch_class_name(
        diatonic_pitch_class_number)
    octave_number = 4 + diatonic_pitch_number // 7
    octave_tick_string = octave_number_to_octave_tick_string(octave_number)
    diatonic_pitch_name = diatonic_pitch_class_name + octave_tick_string

    return diatonic_pitch_name
