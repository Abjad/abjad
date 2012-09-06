def inventory_inversion_equivalent_diatonic_interval_classes():
    '''.. versionadded:: 2.0

    Inventory inversion-equivalent diatonic interval-classes::

        >>> for dic in pitchtools.inventory_inversion_equivalent_diatonic_interval_classes():
        ...     dic
        ...
        InversionEquivalentDiatonicIntervalClass('P1')
        InversionEquivalentDiatonicIntervalClass('aug1')
        InversionEquivalentDiatonicIntervalClass('m2')
        InversionEquivalentDiatonicIntervalClass('M2')
        InversionEquivalentDiatonicIntervalClass('aug2')
        InversionEquivalentDiatonicIntervalClass('dim3')
        InversionEquivalentDiatonicIntervalClass('m3')
        InversionEquivalentDiatonicIntervalClass('M3')
        InversionEquivalentDiatonicIntervalClass('dim4')
        InversionEquivalentDiatonicIntervalClass('P4')
        InversionEquivalentDiatonicIntervalClass('aug4')

    There are 11 inversion-equivalent diatonic interval-classes.

    It is an open question as to whether octaves should be included.

    Return list of inversion-equivalent diatonic interval-classes.
    '''
    from abjad.tools import pitchtools

    return [
        pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 1),
        pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 1),

        pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2),
        pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2),
        pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 2),

        pitchtools.InversionEquivalentDiatonicIntervalClass('diminished', 3),
        pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
        pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),

        pitchtools.InversionEquivalentDiatonicIntervalClass('diminished', 4),
        pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 4),
        pitchtools.InversionEquivalentDiatonicIntervalClass('augmented', 4),
        ]
