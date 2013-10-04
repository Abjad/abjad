# -*- encoding: utf-8 -*-


def pitch_number_to_diatonic_pitch_number(pitch_number):
    '''Change `pitch_number` to diatonic pitch number:

    ::

        >>> pitchtools.pitch_number_to_diatonic_pitch_number(13)
        7

    Return integer.
    '''
    from abjad.tools import pitchtools

    octave = pitch_number // 12
    pitch_class_number = pitch_number % 12

    diatonic_pitch_class_number = pitchtools.pitch_class_number_to_diatonic_pitch_class_number(
        pitch_class_number)

    return 7 * octave + diatonic_pitch_class_number
