# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedInterval___lt___01():
    r'''Compare two ascending chromatic intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(2)
    interval_2 = pitchtools.NumberedInterval(6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1


def test_NumberedInterval___lt___02():
    r'''Compare two descending chromatic intervals.
    '''

    interval_1 = pitchtools.NumberedInterval(-2)
    interval_2 = pitchtools.NumberedInterval(-6)

    assert interval_1 < interval_2
    assert not interval_2 < interval_1
