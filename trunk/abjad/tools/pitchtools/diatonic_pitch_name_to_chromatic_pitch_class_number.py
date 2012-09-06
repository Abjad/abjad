def diatonic_pitch_name_to_chromatic_pitch_class_number(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to chromatic pitch-class number::

        >>> pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("c''")
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    chromatic_pitch_number = pitchtools.diatonic_pitch_name_to_chromatic_pitch_number(diatonic_pitch_name)

    return chromatic_pitch_number % 12
