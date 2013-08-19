# -*- encoding: utf-8 -*-


def instantiate_pitch_and_interval_test_collection():
    r'''Instantiate pitch and interval test collection:

    ::

        >>> for x in pitchtools.instantiate_pitch_and_interval_test_collection(): x
        ...
        HarmonicChromaticInterval(1)
        HarmonicChromaticIntervalClass(1)
        HarmonicDiatonicInterval('M2')
        HarmonicDiatonicIntervalClass('M2')
        NumberedInversionEquivalentIntervalClass(1)
        NamedInversionEquivalentIntervalClass('M2')
        NumberedMelodicInterval(+1)
        NumberedMelodicIntervalClass(+1)
        NamedMelodicInterval('+M2')
        NamedMelodicIntervalClass('+M2')
        NamedPitch('c')
        NamedPitchClass('c')
        NumberedPitch(1)
        NumberedPitchClass(1)

    Use to test pitch and interval interface consistency.

    Return list.
    '''
    from abjad.tools import pitchtools

    result = []
    result.append(pitchtools.HarmonicChromaticInterval(1))
    result.append(pitchtools.HarmonicChromaticIntervalClass(1))
    result.append(pitchtools.HarmonicDiatonicInterval('M2'))
    result.append(pitchtools.HarmonicDiatonicIntervalClass('M2'))
    result.append(pitchtools.NumberedInversionEquivalentIntervalClass(1))
    result.append(pitchtools.NamedInversionEquivalentIntervalClass('M2'))
    result.append(pitchtools.NumberedMelodicInterval(1))
    result.append(pitchtools.NumberedMelodicIntervalClass(1))
    result.append(pitchtools.NamedMelodicInterval('M2'))
    result.append(pitchtools.NamedMelodicIntervalClass('M2'))
    result.append(pitchtools.NamedPitch('c'))
    result.append(pitchtools.NamedPitchClass('c'))
    result.append(pitchtools.NumberedPitch(1))
    result.append(pitchtools.NumberedPitchClass(1))
    return result
