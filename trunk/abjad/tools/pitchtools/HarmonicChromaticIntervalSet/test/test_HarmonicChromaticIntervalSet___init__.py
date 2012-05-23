from abjad import *


def test_HarmonicChromaticIntervalSet___init___01():
    '''Works with interval numbers.'''

    numbers = [0, 1, 14, 15, 28]
    hcis = pitchtools.HarmonicChromaticIntervalSet(numbers)

    assert repr(hcis) == 'HarmonicChromaticIntervalSet(0, 1, 14, 15, 28)'
    assert str(hcis) == '{0, 1, 14, 15, 28}'


def test_HarmonicChromaticIntervalSet___init___02():
    '''Works with interval instances.'''

    numbers = [0, 1, 14, 15, 28]
    intervals = [pitchtools.HarmonicChromaticInterval(x) for x in numbers]
    hcis = pitchtools.HarmonicChromaticIntervalSet(intervals)

    assert repr(hcis) == 'HarmonicChromaticIntervalSet(0, 1, 14, 15, 28)'
    assert str(hcis) == '{0, 1, 14, 15, 28}'
