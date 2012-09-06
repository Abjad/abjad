def chromatic_pitch_class_number_to_diatonic_pitch_class_number(chromatic_pitch_class_number):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_class_number` to diatonic pitch-class number::

        >>> pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(1)
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    chromatic_pitch_class_name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(
        chromatic_pitch_class_number)

    diatonic_pitch_class_name = pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name(
        chromatic_pitch_class_name)

    return pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name)
