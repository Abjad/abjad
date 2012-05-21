from abjad import *


def testMelodicObjectChromaticInterval___lt___01():
    '''Compare two ascending chromatic intervals.'''

    interval_1 = pitchtools.MelodicChromaticInterval(2)
    interval_2 = pitchtools.MelodicChromaticInterval(6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1


def testMelodicObjectChromaticInterval___lt___02():
    '''Compare two descending chromatic intervals.'''

    interval_1 = pitchtools.MelodicChromaticInterval(-2)
    interval_2 = pitchtools.MelodicChromaticInterval(-6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1
