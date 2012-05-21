from abjad.tools.pitchtools import HarmonicChromaticInterval
from abjad.tools.pitchtools import MelodicChromaticIntervalSegment


def testMelodicObjectChromaticIntervalSegment_spread_01():
    mcis = MelodicChromaticIntervalSegment([1, 2, -3, 1, -2, 1])
    assert mcis.spread == HarmonicChromaticInterval(4)


def testMelodicObjectChromaticIntervalSegment_spread_02():
    mcis = MelodicChromaticIntervalSegment([1, 1, 1, 2, -3, -2])
    assert mcis.spread == HarmonicChromaticInterval(5)


def testMelodicObjectChromaticIntervalSegment_spread_03():
    mcis = MelodicChromaticIntervalSegment([1, 1, -2, 2, -3, 1])
    assert mcis.spread == HarmonicChromaticInterval(3)
