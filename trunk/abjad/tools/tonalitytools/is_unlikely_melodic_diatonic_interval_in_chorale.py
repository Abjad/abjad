from abjad.tools import pitchtools


def is_unlikely_melodic_diatonic_interval_in_chorale(mdi):
    '''.. versionadded:: 2.0

    True when `mdi` is unlikely melodic diatonic interval in JSB chorale. ::

        >>> from abjad.tools import tonalitytools

    ::

        >>> mdi = pitchtools.MelodicDiatonicInterval('major', 7)
        >>> tonalitytools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
        True

    Otherwise False. ::

        >>> mdi = pitchtools.MelodicDiatonicInterval('major', 2)
        >>> tonalitytools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
        False

    Return boolean.
    '''

    hdi = mdi.harmonic_diatonic_interval
    hcpi = mdi.harmonic_counterpoint_interval

    acceptable_hdis = pitchtools.HarmonicDiatonicIntervalSet([
        pitchtools.HarmonicDiatonicInterval('augmented', 1),
        pitchtools.HarmonicDiatonicInterval('diminished', 5),
        ])

    if hcpi == pitchtools.HarmonicCounterpointInterval(6):
        return True
    elif hcpi == pitchtools.HarmonicCounterpointInterval(7):
        return True
    elif 8 < hdi.number:
        return True
    elif hdi in acceptable_hdis:
        return False
    elif mdi.quality_string not in ('major', 'minor', 'perfect'):
        return True

    return False
