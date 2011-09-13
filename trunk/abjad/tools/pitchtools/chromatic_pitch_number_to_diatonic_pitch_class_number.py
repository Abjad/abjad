from abjad.tools.pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number import chromatic_pitch_class_number_to_diatonic_pitch_class_number


def chromatic_pitch_number_to_diatonic_pitch_class_number(chromatic_pitch_number):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_number` to diatonic pitch-class number::

        abjad> pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_number(13)
        0

    Return integer.
    '''

    chromatic_pitch_class_number = chromatic_pitch_number % 12

    return chromatic_pitch_class_number_to_diatonic_pitch_class_number(
        chromatic_pitch_class_number)
