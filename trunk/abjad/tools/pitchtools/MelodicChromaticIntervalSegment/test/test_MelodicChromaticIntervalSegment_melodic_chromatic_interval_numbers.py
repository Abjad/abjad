from abjad import *


def test_MelodicChromaticIntervalSegment_melodic_chromatic_interval_numbers_01():
    mciseg = pitchtools.MelodicChromaticIntervalSegment([2, 2, 1, 2, 2, 2, 1])

    assert mciseg.melodic_chromatic_interval_numbers == (2, 2, 1, 2, 2, 2, 1)
