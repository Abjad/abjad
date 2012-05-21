from abjad import *


def testHarmonicObjectChromaticIntervalSet___init___01():
    '''Works with interval numbers.'''

    numbers = [0, 1, 14, 15, 28]
    hcis = pitchtools.HarmonicChromaticIntervalSet(numbers)

    assert repr(hcis) == 'HarmonicChromaticIntervalSet(0, 1, 14, 15, 28)'
    assert str(hcis) == '{0, 1, 14, 15, 28}'


def testHarmonicObjectChromaticIntervalSet___init___02():
    '''Works with interval instances.'''

    numbers = [0, 1, 14, 15, 28]
    intervals = [pitchtools.HarmonicChromaticInterval(x) for x in numbers]
    hcis = pitchtools.HarmonicChromaticIntervalSet(intervals)

    assert repr(hcis) == 'HarmonicChromaticIntervalSet(0, 1, 14, 15, 28)'
    assert str(hcis) == '{0, 1, 14, 15, 28}'
