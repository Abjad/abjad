from abjad.tools.pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number import chromatic_pitch_class_number_to_diatonic_pitch_class_number


def chromatic_pitch_number_to_diatonic_pitch_number(chromatic_pitch_number):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_number` to diatonic pitch number::

        abjad> pitchtools.chromatic_pitch_number_to_diatonic_pitch_number(13)
        7

    Return integer.
    '''

    octave = chromatic_pitch_number // 12
    chromatic_pitch_class_number = chromatic_pitch_number % 12

    diatonic_pitch_class_number = chromatic_pitch_class_number_to_diatonic_pitch_class_number(
        chromatic_pitch_class_number)

    return 7 * octave + diatonic_pitch_class_number
