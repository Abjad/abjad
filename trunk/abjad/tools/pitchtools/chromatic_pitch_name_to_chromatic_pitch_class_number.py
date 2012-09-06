def chromatic_pitch_name_to_chromatic_pitch_class_number(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_class_name` to chromatic pitch-class-number::

        >>> pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("cs''")
        1

    Return integer or float.
    '''
    from abjad.tools import pitchtools

    chromatic_pitch_class_name = pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(
        chromatic_pitch_name)
    chromatic_pitch_class_number = pitchtools.chromatic_pitch_class_name_to_chromatic_pitch_class_number(
        chromatic_pitch_class_name)

    return chromatic_pitch_class_number
