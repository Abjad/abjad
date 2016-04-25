# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval___le___01():
    r'''Compare two ascending numbered intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(2)
    interval_2 = pitchtools.NumberedInterval(6)

    assert interval_1 <= interval_2
    assert not interval_2 <= interval_1


def test_pitchtools_NumberedInterval___le___02():
    r'''Compare two descending numbered intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(-2)
    interval_2 = pitchtools.NumberedInterval(-6)

    assert interval_1 <= interval_2
    assert not interval_2 <= interval_1


def test_pitchtools_NumberedInterval___le___03():
    r'''Compare two ascending numbered intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(2)
    interval_2 = pitchtools.NumberedInterval(2)

    assert interval_1 <= interval_2
    assert interval_2 <= interval_1


def test_pitchtools_NumberedInterval___le___04():
    r'''Compare two descending numbered intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(-2)
    interval_2 = pitchtools.NumberedInterval(-2)

    assert interval_1 <= interval_2
    assert interval_2 <= interval_1
