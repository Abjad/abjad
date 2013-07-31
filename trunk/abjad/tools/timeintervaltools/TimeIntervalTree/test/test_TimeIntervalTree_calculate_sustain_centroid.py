# -*- encoding: utf-8 -*-
from abjad import *


def test_TimeIntervalTree_calculate_sustain_centroid_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    result = tree.calculate_sustain_centroid()
    assert result == Multiplier(1619, 90)


def test_TimeIntervalTree_calculate_sustain_centroid_02():
    tree = timeintervaltools.TimeIntervalTree([])
    result = tree.calculate_sustain_centroid()
    assert result is None
