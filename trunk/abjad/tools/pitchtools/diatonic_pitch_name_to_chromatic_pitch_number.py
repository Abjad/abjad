def diatonic_pitch_name_to_chromatic_pitch_number(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to chromatic pitch number::

        >>> pitchtools.diatonic_pitch_name_to_chromatic_pitch_number("c''")
        12

    Return integer.
    '''
    from abjad.tools import pitchtools

    diatonic_pitch_number = pitchtools.diatonic_pitch_name_to_diatonic_pitch_number(diatonic_pitch_name)

    return pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(diatonic_pitch_number)
