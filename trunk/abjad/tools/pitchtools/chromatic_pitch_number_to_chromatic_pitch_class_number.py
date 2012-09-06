def chromatic_pitch_number_to_chromatic_pitch_class_number(chromatic_pitch_number):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_number` to chromatic pitch-class number::

        >>> pitchtools.chromatic_pitch_number_to_chromatic_pitch_class_number(13)
        1

    Return integer or float.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.is_chromatic_pitch_number(chromatic_pitch_number):
        raise TypeError

    return chromatic_pitch_number % 12
