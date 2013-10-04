# -*- encoding: utf-8 -*-


def pitch_number_to_diatonic_pitch_class_number(pitch_number):
    '''Change `pitch_number` to diatonic pitch-class number:

    ::

        >>> pitchtools.pitch_number_to_diatonic_pitch_class_number(13)
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    pitch_class_number = pitch_number % 12

    return pitchtools.pitch_class_number_to_diatonic_pitch_class_number(
        pitch_class_number)
