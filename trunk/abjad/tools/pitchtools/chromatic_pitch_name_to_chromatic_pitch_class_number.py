from abjad.tools.pitchtools.chromatic_pitch_class_name_to_chromatic_pitch_class_number import chromatic_pitch_class_name_to_chromatic_pitch_class_number
from abjad.tools.pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name import chromatic_pitch_name_to_chromatic_pitch_class_name


def chromatic_pitch_name_to_chromatic_pitch_class_number(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_class_name` to chromatic pitch-class-number::

        abjad> pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("cs''")
        1

    Return integer or float.
    '''

    chromatic_pitch_class_name = chromatic_pitch_name_to_chromatic_pitch_class_name(
        chromatic_pitch_name)
    chromatic_pitch_class_number = chromatic_pitch_class_name_to_chromatic_pitch_class_number(
        chromatic_pitch_class_name)

    return chromatic_pitch_class_number
