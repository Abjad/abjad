from abjad import *


def test_MelodicChromaticIntervalSegment_slope_01():
    mcis = pitchtools.MelodicChromaticIntervalSegment([1])
    assert mcis.slope == 1


def test_MelodicChromaticIntervalSegment_slope_02():
    mcis = pitchtools.MelodicChromaticIntervalSegment([-2, 1])
    assert mcis.slope == Fraction(-1, 2)


def test_MelodicChromaticIntervalSegment_slope_03():
    mcis = pitchtools.MelodicChromaticIntervalSegment([1, 2, -3, 0, 2, -1, -1.5, 0.5])
    assert mcis.slope == 0
