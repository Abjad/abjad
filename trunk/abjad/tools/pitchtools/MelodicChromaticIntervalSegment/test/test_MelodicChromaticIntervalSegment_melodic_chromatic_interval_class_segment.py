from abjad import *


def test_MelodicChromaticIntervalSegment_melodic_chromatic_interval_class_segment_01():

    mciseg = pitchtools.MelodicChromaticIntervalSegment([2, 2, 13, 2, 2, 14, 1])
    "MelodicChromaticIntervalSegment(+2, +2, +13, +2, +2, +14, +1)"
    mcicseg = mciseg.melodic_chromatic_interval_class_segment

    numbers = [2, 2, 1, 2, 2, 2, 1]
    assert mcicseg == pitchtools.MelodicChromaticIntervalClassSegment(numbers)
