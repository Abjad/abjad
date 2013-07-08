from abjad import *
from abjad.tools.timeintervaltools import TimeIntervalTree


def test_timeintervaltools_calculate_min_mean_and_max_depth_of_intervals_01():
    tree = TimeIntervalTree([])
    result = timeintervaltools.calculate_min_mean_and_max_depth_of_intervals(
        tree)
    assert result is None


def test_timeintervaltools_calculate_min_mean_and_max_depth_of_intervals_02():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    result = timeintervaltools.calculate_min_mean_and_max_depth_of_intervals(
        tree)
    assert result == (0, Fraction(45, 37), 3)
