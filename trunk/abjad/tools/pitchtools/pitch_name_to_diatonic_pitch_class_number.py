# -*- encoding: utf-8 -*-


def pitch_name_to_diatonic_pitch_class_number(pitch_name):
    '''Change `pitch_name` to diatonic pitch-class number:

    ::

        >>> pitchtools.pitch_name_to_diatonic_pitch_class_number("cs''")
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    diatonic_pitch_number = pitchtools.pitch_name_to_diatonic_pitch_number(pitch_name)
    diatonic_pitch_class_number = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(
        diatonic_pitch_number)

    return diatonic_pitch_class_number
