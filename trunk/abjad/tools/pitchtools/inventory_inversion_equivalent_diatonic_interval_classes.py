from abjad.tools.pitchtools.InversionEquivalentDiatonicIntervalClass import InversionEquivalentDiatonicIntervalClass


def inventory_inversion_equivalent_diatonic_interval_classes():
    '''.. versionadded:: 2.0

    Inventory inversion-equivalent diatonic interval-classes::

        abjad> for dic in pitchtools.inventory_inversion_equivalent_diatonic_interval_classes():
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

    return [
        InversionEquivalentDiatonicIntervalClass('perfect', 1),
        InversionEquivalentDiatonicIntervalClass('augmented', 1),

        InversionEquivalentDiatonicIntervalClass('minor', 2),
        InversionEquivalentDiatonicIntervalClass('major', 2),
        InversionEquivalentDiatonicIntervalClass('augmented', 2),

        InversionEquivalentDiatonicIntervalClass('diminished', 3),
        InversionEquivalentDiatonicIntervalClass('minor', 3),
        InversionEquivalentDiatonicIntervalClass('major', 3),

        InversionEquivalentDiatonicIntervalClass('diminished', 4),
        InversionEquivalentDiatonicIntervalClass('perfect', 4),
        InversionEquivalentDiatonicIntervalClass('augmented', 4),
        ]
