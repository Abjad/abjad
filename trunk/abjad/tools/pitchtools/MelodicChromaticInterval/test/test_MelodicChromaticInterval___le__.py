from abjad import *


def test_MelodicChromaticInterval___le___01():
    '''Compare two ascending chromatic intervals.'''

    interval_1 = pitchtools.MelodicChromaticInterval(2)
    interval_2 = pitchtools.MelodicChromaticInterval(6)

    assert interval_1 <= interval_2
    assert not interval_2 <= interval_1


def test_MelodicChromaticInterval___le___02():
    '''Compare two descending chromatic intervals.'''

    interval_1 = pitchtools.MelodicChromaticInterval(-2)
    interval_2 = pitchtools.MelodicChromaticInterval(-6)

    assert interval_1 <= interval_2
    assert not interval_2 <= interval_1


def test_MelodicChromaticInterval___le___03():
    '''Compare two ascending chromatic intervals.'''

    interval_1 = pitchtools.MelodicChromaticInterval(2)
    interval_2 = pitchtools.MelodicChromaticInterval(2)

    assert interval_1 <= interval_2
    assert interval_2 <= interval_1


def test_MelodicChromaticInterval___le___04():
    '''Compare two descending chromatic intervals.'''

    interval_1 = pitchtools.MelodicChromaticInterval(-2)
    interval_2 = pitchtools.MelodicChromaticInterval(-2)

    assert interval_1 <= interval_2
    assert interval_2 <= interval_1
