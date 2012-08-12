def calculate_harmonic_diatonic_interval_class(pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate harmonic diatonic interval-class from `pitch_carrier_1` to
    `pitch_carrier_2`::

        >>> pitchtools.calculate_harmonic_diatonic_interval_class(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        HarmonicDiatonicIntervalClass('M2')

    Return harmonic diatonic interval-class.
    '''
    from abjad.tools import pitchtools

    # get melodic diatonic interval
    mdi = pitchtools.calculate_melodic_diatonic_interval(
        pitch_carrier_1, pitch_carrier_2)

    # return harmonic diatonic interval-class
    return mdi.harmonic_diatonic_interval.harmonic_diatonic_interval_class
