# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_inventory_named_inversion_equivalent_interval_classes_01():

    all_dics = pitchtools.inventory_named_inversion_equivalent_interval_classes()

    assert all_dics == [
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
