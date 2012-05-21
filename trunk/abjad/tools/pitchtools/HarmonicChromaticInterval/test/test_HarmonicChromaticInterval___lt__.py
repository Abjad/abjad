from abjad import *


def testHarmonicObjectChromaticInterval___lt___01():
    '''Compare two ascending chromatic intervals.'''

    interval_1 = pitchtools.HarmonicChromaticInterval(2)
    interval_2 = pitchtools.HarmonicChromaticInterval(6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1


def testHarmonicObjectChromaticInterval___lt___02():
    '''Compare two descending chromatic intervals.'''

    interval_1 = pitchtools.HarmonicChromaticInterval(-2)
    interval_2 = pitchtools.HarmonicChromaticInterval(-6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1
