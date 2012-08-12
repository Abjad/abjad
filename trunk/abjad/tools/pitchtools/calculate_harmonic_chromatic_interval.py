def calculate_harmonic_chromatic_interval(pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate harmonic chromatic interval from `pitch_carrier_1` to
    `pitch_carrier_2`::

        >>> pitchtools.calculate_harmonic_chromatic_interval(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        HarmonicChromaticInterval(14)

    Return harmonic chromatic interval.
    '''
    from abjad.tools import pitchtools

    # get melodic chromatic interval
    mci = pitchtools.calculate_melodic_chromatic_interval(
        pitch_carrier_1, pitch_carrier_2)

    # return harmonic chromatic interval
    return mci.harmonic_chromatic_interval
