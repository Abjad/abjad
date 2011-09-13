from abjad import *


def test_InversionEquivalentChromaticIntervalClassSet___init___01():

    ics = pitchtools.InversionEquivalentChromaticIntervalClassSet([1, 5, 1, 1, 3])
    assert ics.inversion_equivalent_chromatic_interval_class_numbers == set([1, 3, 5])
