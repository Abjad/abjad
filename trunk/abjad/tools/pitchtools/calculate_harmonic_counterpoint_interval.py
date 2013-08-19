# -*- encoding: utf-8 -*-


def calculate_harmonic_counterpoint_interval(pitch_carrier_1, pitch_carrier_2):
    '''Calculate harmonic counterpoint interval `pitch_carrier_1` to
    `pitch_carrier_2`:

    ::

        >>> pitchtools.calculate_harmonic_counterpoint_interval(
        ... pitchtools.NamedChromaticPitch(-2), pitchtools.NamedChromaticPitch(12))
        HarmonicCounterpointInterval(9)

    Return harmonic counterpoint interval-class.
    '''
    from abjad.tools import pitchtools

    # get melodic diatonic interval
    mdi = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitch_carrier_1, pitch_carrier_2)

    # return harmonic counterpoint interval
    return mdi.harmonic_counterpoint_interval
