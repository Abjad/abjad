# -*- coding: utf-8 -*-


def instantiate_pitch_and_interval_test_collection():
    r'''Instantiates pitch and interval test collection.

    ::

        >>> for x in pitchtools.instantiate_pitch_and_interval_test_collection(): x
        ...
        NumberedInversionEquivalentIntervalClass(1)
        NamedInversionEquivalentIntervalClass('+M2')
        NumberedInterval(1)
        NumberedIntervalClass(1)
        NamedInterval('+M2')
        NamedIntervalClass('+M2')
        NamedPitch('c')
        NamedPitchClass('c')
        NumberedPitch(1)
        NumberedPitchClass(1)

    Use to test pitch and interval interface consistency.

    Returns list.
    '''
    from abjad.tools import pitchtools

    result = []
    result.append(pitchtools.NumberedInversionEquivalentIntervalClass(1))
    result.append(pitchtools.NamedInversionEquivalentIntervalClass('M2'))
    result.append(pitchtools.NumberedInterval(1))
    result.append(pitchtools.NumberedIntervalClass(1))
    result.append(pitchtools.NamedInterval('M2'))
    result.append(pitchtools.NamedIntervalClass('M2'))
    result.append(pitchtools.NamedPitch('c'))
    result.append(pitchtools.NamedPitchClass('c'))
    result.append(pitchtools.NumberedPitch(1))
    result.append(pitchtools.NumberedPitchClass(1))
    return result