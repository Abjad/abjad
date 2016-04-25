# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval___lt___01():
    r'''Compare two ascending numbered intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(2)
    interval_2 = pitchtools.NumberedInterval(6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1


def test_pitchtools_NumberedInterval___lt___02():
    r'''Compare two descending numbered intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(-2)
    interval_2 = pitchtools.NumberedInterval(-6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1
