from abjad import *


def test_MelodicChromaticIntervalClassSegment___init___01():

    mcic_numbers = [2, 2, 13, 2, 2, 14, 1]
    mcicseg = pitchtools.MelodicChromaticIntervalClassSegment(mcic_numbers)

    "MelodicChromaticIntervalClassSegment(+2, +2, +1, +2, +2, +2, +1)"

    assert mcicseg.interval_class_numbers == (2, 2, 1, 2, 2, 2, 1)
