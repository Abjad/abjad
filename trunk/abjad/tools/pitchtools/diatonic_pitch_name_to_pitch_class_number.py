# -*- encoding: utf-8 -*-


def diatonic_pitch_name_to_pitch_class_number(diatonic_pitch_name):
    '''Change `diatonic_pitch_name` to chromatic pitch-class number:

    ::

        >>> pitchtools.diatonic_pitch_name_to_pitch_class_number("c''")
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    pitch_number = pitchtools.diatonic_pitch_name_to_pitch_number(diatonic_pitch_name)

    return pitch_number % 12
