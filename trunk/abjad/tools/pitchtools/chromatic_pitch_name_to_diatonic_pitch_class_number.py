from abjad.tools.pitchtools.chromatic_pitch_name_to_diatonic_pitch_number import chromatic_pitch_name_to_diatonic_pitch_number
from abjad.tools.pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number import diatonic_pitch_number_to_diatonic_pitch_class_number


def chromatic_pitch_name_to_diatonic_pitch_class_number(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_name` to diatonic pitch-class number::

        abjad> pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_number("cs''")
        0

    Return integer.
    '''

    diatonic_pitch_number = chromatic_pitch_name_to_diatonic_pitch_number(chromatic_pitch_name)
    diatonic_pitch_class_number = diatonic_pitch_number_to_diatonic_pitch_class_number(
        diatonic_pitch_number)

    return diatonic_pitch_class_number
