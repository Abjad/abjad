from abjad import *


def test_NumberedChromaticPitchClassSet_inversion_equivalent_chromatic_interval_class_set_01():

    pcset = pitchtools.NumberedChromaticPitchClassSet([0, 6, 10, 4, 9, 2])

    iecics = pitchtools.InversionEquivalentChromaticIntervalClassSet([1, 2, 3, 4, 5, 6])
    assert pcset.inversion_equivalent_chromatic_interval_class_set == iecics
