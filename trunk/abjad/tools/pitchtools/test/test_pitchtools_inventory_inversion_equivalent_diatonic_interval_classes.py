from abjad import *


def test_pitchtools_inventory_inversion_equivalent_diatonic_interval_classes_01():

    all_dics = pitchtools.inventory_inversion_equivalent_diatonic_interval_classes()

    assert all_dics == [
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
