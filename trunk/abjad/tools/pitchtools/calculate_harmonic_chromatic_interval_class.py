def calculate_harmonic_chromatic_interval_class(pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate harmonic chromatic interval-class from `pitch_carrier_1` to
    `pitch_carrier_2`::

        >>> pitchtools.calculate_harmonic_chromatic_interval_class(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        HarmonicChromaticIntervalClass(2)

    Return harmonic chromatic interval-class.
    '''
    from abjad.tools import pitchtools

    # get melodic chromatic interval
    mci = pitchtools.calculate_melodic_chromatic_interval(
        pitch_carrier_1, pitch_carrier_2)

    # return harmonic chromatic interval-class
    return mci.harmonic_chromatic_interval.harmonic_chromatic_interval_class
