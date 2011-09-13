def instantiate_pitch_and_interval_test_collection():
    r'''.. versionadded:: 2.0

    Instantiate pitch and interval test collection::

        abjad> for x in pitchtools.instantiate_pitch_and_interval_test_collection(): x
        ...
        HarmonicChromaticInterval(1)
        HarmonicChromaticIntervalClass(1)
        HarmonicCounterpointInterval(1)
        HarmonicCounterpointIntervalClass(1)
        HarmonicDiatonicInterval('M2')
        HarmonicDiatonicIntervalClass('M2')
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentDiatonicIntervalClass('M2')
        MelodicChromaticInterval(+1)
        MelodicChromaticIntervalClass(+1)
        MelodicCounterpointInterval(1)
        MelodicCounterpointIntervalClass(+1)
        MelodicDiatonicInterval('+M2')
        MelodicDiatonicIntervalClass('+M2')
        NamedChromaticPitch('c')
        NamedChromaticPitchClass('c')
        NamedDiatonicPitch('c')
        NamedDiatonicPitchClass('c')
        NumberedChromaticPitch(1)
        NumberedChromaticPitchClass(1)
        NumberedDiatonicPitch(1)
        NumberedDiatonicPitchClass(1)

    Use to test pitch and interval interface consistency.

    Return list.
    '''
    from abjad.tools import pitchtools

    result = []
    result.append(pitchtools.HarmonicChromaticInterval(1))
    result.append(pitchtools.HarmonicChromaticIntervalClass(1))
    result.append(pitchtools.HarmonicCounterpointInterval(1))
    result.append(pitchtools.HarmonicCounterpointIntervalClass(1))
    result.append(pitchtools.HarmonicDiatonicInterval('M2'))
    result.append(pitchtools.HarmonicDiatonicIntervalClass('M2'))
    result.append(pitchtools.InversionEquivalentChromaticIntervalClass(1))
    result.append(pitchtools.InversionEquivalentDiatonicIntervalClass('M2'))
    result.append(pitchtools.MelodicChromaticInterval(1))
    result.append(pitchtools.MelodicChromaticIntervalClass(1))
    result.append(pitchtools.MelodicCounterpointInterval(1))
    result.append(pitchtools.MelodicCounterpointIntervalClass(1))
    result.append(pitchtools.MelodicDiatonicInterval('M2'))
    result.append(pitchtools.MelodicDiatonicIntervalClass('M2'))
    result.append(pitchtools.NamedChromaticPitch('c'))
    result.append(pitchtools.NamedChromaticPitchClass('c'))
    result.append(pitchtools.NamedDiatonicPitch('c'))
    result.append(pitchtools.NamedDiatonicPitchClass('c'))
    result.append(pitchtools.NumberedChromaticPitch(1))
    result.append(pitchtools.NumberedChromaticPitchClass(1))
    result.append(pitchtools.NumberedDiatonicPitch(1))
    result.append(pitchtools.NumberedDiatonicPitchClass(1))
    return result
