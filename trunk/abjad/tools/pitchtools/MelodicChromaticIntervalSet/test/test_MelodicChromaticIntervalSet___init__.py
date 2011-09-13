from abjad import *


def test_MelodicChromaticIntervalSet___init___01():
    '''Works with interval numbers.'''

    mcis = pitchtools.MelodicChromaticIntervalSet([-13, -12, -11, 0, 1, 19])

    assert repr(mcis) == 'MelodicChromaticIntervalSet(-13, -12, -11, 0, +1, +19)'
    assert str(mcis) == '{-13, -12, -11, 0, +1, +19}'
    assert len(mcis) == 6


def test_MelodicChromaticIntervalSet___init___02():
    '''Works with interval instances.'''

    numbers = [-13, -12, -11, 0, 1, 19]
    intervals = [pitchtools.MelodicChromaticInterval(x) for x in numbers]
    mcis = pitchtools.MelodicChromaticIntervalSet(intervals)

    assert repr(mcis) == 'MelodicChromaticIntervalSet(-13, -12, -11, 0, +1, +19)'
    assert str(mcis) == '{-13, -12, -11, 0, +1, +19}'
    assert len(mcis) == 6
