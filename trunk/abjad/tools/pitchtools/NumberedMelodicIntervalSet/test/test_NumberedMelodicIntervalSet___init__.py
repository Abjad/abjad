# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicIntervalSet___init___01():
    r'''Works with interval numbers.
    '''

    mcis = pitchtools.NumberedMelodicIntervalSet([-13, -12, -11, 0, 1, 19])

    assert repr(mcis) == 'NumberedMelodicIntervalSet(-13, -12, -11, 0, +1, +19)'
    assert str(mcis) == '{-13, -12, -11, 0, +1, +19}'
    assert len(mcis) == 6


def test_NumberedMelodicIntervalSet___init___02():
    r'''Works with interval instances.
    '''

    numbers = [-13, -12, -11, 0, 1, 19]
    intervals = [pitchtools.NumberedMelodicInterval(x) for x in numbers]
    mcis = pitchtools.NumberedMelodicIntervalSet(intervals)

    assert repr(mcis) == 'NumberedMelodicIntervalSet(-13, -12, -11, 0, +1, +19)'
    assert str(mcis) == '{-13, -12, -11, 0, +1, +19}'
    assert len(mcis) == 6
