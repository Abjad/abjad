def calculate_melodic_counterpoint_interval(pitch_carrier_1, pitch_carrier_2):
    '''.. versionadded:: 2.0

    Calculate melodic counterpoint interval `pitch_carrier_1` to
    `pitch_carrier_2`::

        >>> pitchtools.calculate_melodic_counterpoint_interval(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        MelodicCounterpointInterval(+9)

    Return melodic counterpoint interval.
    '''
    from abjad.tools import pitchtools

    # get melodic diatonic interval
    mdi = pitchtools.calculate_melodic_diatonic_interval(pitch_carrier_1, pitch_carrier_2)

    # return melodic counterpoint interval
    return mdi.melodic_counterpoint_interval
