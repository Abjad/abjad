# -*- encoding: utf-8 -*-


def chromatic_pitch_name_to_pitch_class_number(chromatic_pitch_name):
    '''Change `chromatic_class_name` to chromatic pitch-class-number:

    ::

        >>> pitchtools.chromatic_pitch_name_to_pitch_class_number("cs''")
        1

    Return integer or float.
    '''
    from abjad.tools import pitchtools

    pitch_class_name = pitchtools.chromatic_pitch_name_to_pitch_class_name(
        chromatic_pitch_name)
    pitch_class_number = pitchtools.pitch_class_name_to_pitch_class_number(
        pitch_class_name)

    return pitch_class_number
