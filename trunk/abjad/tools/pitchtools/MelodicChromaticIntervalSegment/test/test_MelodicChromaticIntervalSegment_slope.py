from abjad.tools.pitchtools import MelodicChromaticIntervalSegment
from fractions import Fraction


def testMelodicObjectChromaticIntervalSegment_slope_01():
    mcis = MelodicChromaticIntervalSegment([1])
    assert mcis.slope == 1

def testMelodicObjectChromaticIntervalSegment_slope_02():
    mcis = MelodicChromaticIntervalSegment([-2, 1])
    assert mcis.slope == Fraction(-1, 2)

def testMelodicObjectChromaticIntervalSegment_slope_03():
    mcis = MelodicChromaticIntervalSegment([1, 2, -3, 0, 2, -1, -1.5, 0.5])
    assert mcis.slope == 0
