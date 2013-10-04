# -*- encoding: utf-8 -*-


def pitch_name_to_pitch_class_number(pitch_name):
    '''Change `chromatic_class_name` to chromatic pitch-class-number:

    ::

        >>> pitchtools.pitch_name_to_pitch_class_number("cs''")
        1

    Return integer or float.
    '''
    from abjad.tools import pitchtools

    pitch_class_name = pitchtools.pitch_name_to_pitch_class_name(
        pitch_name)
    pitch_class_number = pitchtools.pitch_class_name_to_pitch_class_number(
        pitch_class_name)

    return pitch_class_number
