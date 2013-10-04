# -*- encoding: utf-8 -*-


def chromatic_pitch_number_to_diatonic_pitch_class_number(chromatic_pitch_number):
    '''Change `chromatic_pitch_number` to diatonic pitch-class number:

    ::

        >>> pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_number(13)
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    pitch_class_number = chromatic_pitch_number % 12

    return pitchtools.pitch_class_number_to_diatonic_pitch_class_number(
        pitch_class_number)
