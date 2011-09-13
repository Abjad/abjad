from abjad.tools.pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number import diatonic_pitch_class_name_to_diatonic_pitch_class_number
from abjad.tools.pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_name import diatonic_pitch_name_to_diatonic_pitch_class_name


def diatonic_pitch_name_to_diatonic_pitch_class_number(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to diatonic pitch-class number::

        abjad> pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_number("c''")
        0

    Return integer.
    '''

    diatonic_pitch_class_name = diatonic_pitch_name_to_diatonic_pitch_class_name(diatonic_pitch_name)

    return diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name)
