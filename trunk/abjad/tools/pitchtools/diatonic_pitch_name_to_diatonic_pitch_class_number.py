def diatonic_pitch_name_to_diatonic_pitch_class_number(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to diatonic pitch-class number::

        >>> pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_number("c''")
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    diatonic_pitch_class_name = pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_name(
        diatonic_pitch_name)

    return pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name)
