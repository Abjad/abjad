def calculate_melodic_diatonic_interval(pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic diatonic interval from `pitch_carrier_1` to
    `pitch_carrier_2`::

        >>> pitchtools.calculate_melodic_diatonic_interval(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicDiatonicInterval('+M9')

    Return melodic diatonic interval.
    '''
    from abjad.tools import pitchtools

    pitch_1 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
    pitch_2 = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)

    degree_1 = abs(pitch_1.numbered_diatonic_pitch)
    degree_2 = abs(pitch_2.numbered_diatonic_pitch)

    diatonic_interval_number = abs(degree_1 - degree_2) + 1

    chromatic_interval_number = abs(abs(pitch_1.numbered_chromatic_pitch) -
        abs(pitch_2.numbered_chromatic_pitch))

    absolute_diatonic_interval = \
        pitchtools.spell_chromatic_interval_number(
        diatonic_interval_number, chromatic_interval_number)

    if pitch_2 < pitch_1:
        diatonic_interval = -absolute_diatonic_interval
    else:
        diatonic_interval = absolute_diatonic_interval

    return diatonic_interval
