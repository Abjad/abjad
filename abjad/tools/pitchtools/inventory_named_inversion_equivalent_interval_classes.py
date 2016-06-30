# -*- coding: utf-8 -*-


def inventory_named_inversion_equivalent_interval_classes():
    '''Inventories named inversion-equivalent interval-classes.

    ::

        >>> for dic in pitchtools.inventory_named_inversion_equivalent_interval_classes():
        ...     dic
        ...
        NamedInversionEquivalentIntervalClass('P1')
        NamedInversionEquivalentIntervalClass('aug1')
        NamedInversionEquivalentIntervalClass('+m2')
        NamedInversionEquivalentIntervalClass('+M2')
        NamedInversionEquivalentIntervalClass('+aug2')
        NamedInversionEquivalentIntervalClass('+dim3')
        NamedInversionEquivalentIntervalClass('+m3')
        NamedInversionEquivalentIntervalClass('+M3')
        NamedInversionEquivalentIntervalClass('+dim4')
        NamedInversionEquivalentIntervalClass('+P4')
        NamedInversionEquivalentIntervalClass('+aug4')

    There are 11 named inversion-equivalent interval-classes.

    It is an open question as to whether octaves should be included.

    Returns list of named inversion-equivalent interval-classes.
    '''
    from abjad.tools import pitchtools

    return [
        pitchtools.NamedInversionEquivalentIntervalClass('perfect', 1),
        pitchtools.NamedInversionEquivalentIntervalClass('augmented', 1),

        pitchtools.NamedInversionEquivalentIntervalClass('minor', 2),
        pitchtools.NamedInversionEquivalentIntervalClass('major', 2),
        pitchtools.NamedInversionEquivalentIntervalClass('augmented', 2),

        pitchtools.NamedInversionEquivalentIntervalClass('diminished', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),

        pitchtools.NamedInversionEquivalentIntervalClass('diminished', 4),
        pitchtools.NamedInversionEquivalentIntervalClass('perfect', 4),
        pitchtools.NamedInversionEquivalentIntervalClass('augmented', 4),
        ]