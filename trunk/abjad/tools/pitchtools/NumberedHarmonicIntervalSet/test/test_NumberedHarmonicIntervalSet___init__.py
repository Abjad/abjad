# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedHarmonicIntervalSet___init___01():
    r'''Works with interval numbers.
    '''

    numbers = [0, 1, 14, 15, 28]
    hcis = pitchtools.NumberedHarmonicIntervalSet(numbers)

    assert repr(hcis) == 'NumberedHarmonicIntervalSet(0, 1, 14, 15, 28)'
    assert str(hcis) == '{0, 1, 14, 15, 28}'


def test_NumberedHarmonicIntervalSet___init___02():
    r'''Works with interval instances.
    '''

    numbers = [0, 1, 14, 15, 28]
    intervals = [pitchtools.NumberedHarmonicInterval(x) for x in numbers]
    hcis = pitchtools.NumberedHarmonicIntervalSet(intervals)

    assert repr(hcis) == 'NumberedHarmonicIntervalSet(0, 1, 14, 15, 28)'
    assert str(hcis) == '{0, 1, 14, 15, 28}'
