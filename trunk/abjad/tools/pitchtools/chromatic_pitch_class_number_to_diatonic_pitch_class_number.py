from abjad.tools.pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name import chromatic_pitch_class_name_to_diatonic_pitch_class_name
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name import chromatic_pitch_class_number_to_chromatic_pitch_class_name
from abjad.tools.pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number import diatonic_pitch_class_name_to_diatonic_pitch_class_number


def chromatic_pitch_class_number_to_diatonic_pitch_class_number(chromatic_pitch_class_number):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_class_number` to diatonic pitch-class number::

        abjad> pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(1)
        0

    Return integer.
    '''

    chromatic_pitch_class_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name(
        chromatic_pitch_class_number)

    diatonic_pitch_class_name = chromatic_pitch_class_name_to_diatonic_pitch_class_name(
        chromatic_pitch_class_name)

    return diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name)
