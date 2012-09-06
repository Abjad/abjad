def chromatic_pitch_name_to_diatonic_pitch_class_name(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_name` to diatonic pitch name::

        >>> pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name("cs''")
        'c'

    Return string.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.is_chromatic_pitch_name(chromatic_pitch_name):
        raise ValueError('\n\tNote chromatic pitch name: "%s".' % chromatic_pitch_name)

    return chromatic_pitch_name[0]
