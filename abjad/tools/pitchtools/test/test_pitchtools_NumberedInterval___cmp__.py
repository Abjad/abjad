# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval___cmp___01():

    numbered_interval_1 = pitchtools.NumberedInterval(12)
    numbered_interval_2 = pitchtools.NumberedInterval(12)
    numbered_interval_3 = pitchtools.NumberedInterval(13)

    assert numbered_interval_1 == numbered_interval_1
    assert not numbered_interval_1 != numbered_interval_1
    assert not numbered_interval_1 < numbered_interval_1
    assert numbered_interval_1 <= numbered_interval_1
    assert not numbered_interval_1 > numbered_interval_1
    assert numbered_interval_1 >= numbered_interval_1

    assert numbered_interval_1 == numbered_interval_2
    assert not numbered_interval_1 != numbered_interval_2
    assert not numbered_interval_1 < numbered_interval_2
    assert numbered_interval_1 <= numbered_interval_2
    assert not numbered_interval_1 > numbered_interval_2
    assert numbered_interval_1 >= numbered_interval_2

    assert not numbered_interval_1 == numbered_interval_3
    assert numbered_interval_1 != numbered_interval_3
    assert numbered_interval_1 < numbered_interval_3
    assert numbered_interval_1 <= numbered_interval_3
    assert not numbered_interval_1 > numbered_interval_3
    assert not numbered_interval_1 >= numbered_interval_3
