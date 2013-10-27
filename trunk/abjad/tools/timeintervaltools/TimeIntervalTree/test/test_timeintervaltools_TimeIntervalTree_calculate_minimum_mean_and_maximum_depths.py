# -*- encoding: utf-8 -*-
from abjad import *


def test_timeintervaltools_TimeIntervalTree_calculate_minimum_mean_and_maximum_depths_01():
    tree = timeintervaltools.TimeIntervalTree([])
    result = tree.calculate_minimum_mean_and_maximum_depths()
    assert result is None


def test_timeintervaltools_TimeIntervalTree_calculate_minimum_mean_and_maximum_depths_02():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    result = tree.calculate_minimum_mean_and_maximum_depths()
    assert result == (0, Fraction(45, 37), 3)
