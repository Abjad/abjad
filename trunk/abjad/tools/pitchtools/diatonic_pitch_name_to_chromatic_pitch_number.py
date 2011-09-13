from abjad.tools.pitchtools.diatonic_pitch_name_to_diatonic_pitch_number import diatonic_pitch_name_to_diatonic_pitch_number
from abjad.tools.pitchtools.diatonic_pitch_number_to_chromatic_pitch_number import diatonic_pitch_number_to_chromatic_pitch_number


def diatonic_pitch_name_to_chromatic_pitch_number(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to chromatic pitch number::

        abjad> pitchtools.diatonic_pitch_name_to_chromatic_pitch_number("c''")
        12

    Return integer.
    '''

    diatonic_pitch_number = diatonic_pitch_name_to_diatonic_pitch_number(diatonic_pitch_name)

    return diatonic_pitch_number_to_chromatic_pitch_number(diatonic_pitch_number)
