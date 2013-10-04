# -*- encoding: utf-8 -*-


def pitch_number_to_pitch_class_number(pitch_number):
    '''Change `pitch_number` to chromatic pitch-class number:

    ::

        >>> pitchtools.pitch_number_to_pitch_class_number(13)
        1

    Return integer or float.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.is_pitch_number(pitch_number):
        raise TypeError

    return pitch_number % 12
