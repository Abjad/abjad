from abjad.tools import pitchtools


def is_unlikely_melodic_diatonic_interval_in_chorale(mdi):
    '''.. versionadded:: 2.0

    True when `mdi` is unlikely melodic diatonic interval in JSB chorale. ::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> mdi = pitchtools.MelodicDiatonicInterval('major', 7)
        abjad> tonalitytools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
        True

    Otherwise False. ::

        abjad> mdi = pitchtools.MelodicDiatonicInterval('major', 2)
        abjad> tonalitytools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
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
