def calculate_melodic_chromatic_interval_class(pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic chromatic interval-class from `pitch_carrier_1` to
    `pitch_carrier_2`::

        >>> pitchtools.calculate_melodic_chromatic_interval_class(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicChromaticIntervalClass(+2)

    Return melodic chromatic interval-class.
    '''
    from abjad.tools import pitchtools

    # get melodic chromatic interval
    mci = pitchtools.calculate_melodic_chromatic_interval(pitch_carrier_1, pitch_carrier_2)

    # return melodic chromatic interval-class
    return mci.melodic_chromatic_interval_class
