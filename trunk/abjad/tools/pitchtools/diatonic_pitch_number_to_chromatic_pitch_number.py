from abjad.tools.pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number import diatonic_pitch_class_number_to_chromatic_pitch_class_number


def diatonic_pitch_number_to_chromatic_pitch_number(diatonic_pitch_number):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_number` to chromatic pitch number::

        abjad> pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(7)
        12

    Return integer.
    '''

    octave = diatonic_pitch_number // 7

    diatonic_pitch_class_number = diatonic_pitch_number % 7
    chromatic_pitch_class_number = diatonic_pitch_class_number_to_chromatic_pitch_class_number(
        diatonic_pitch_class_number)

    return octave * 12 + chromatic_pitch_class_number
