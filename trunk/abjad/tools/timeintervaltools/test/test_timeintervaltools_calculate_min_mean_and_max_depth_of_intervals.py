from abjad.tools.timeintervaltools import TimeIntervalTree
from abjad.tools.timeintervaltools import calculate_min_mean_and_max_depth_of_intervals
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction


def test_timeintervaltools_calculate_min_mean_and_max_depth_of_intervals_01():
    tree = TimeIntervalTree([])
    result = calculate_min_mean_and_max_depth_of_intervals(tree)
    assert result is None


def test_timeintervaltools_calculate_min_mean_and_max_depth_of_intervals_02():
    tree = TimeIntervalTree(_make_test_intervals())
    result = calculate_min_mean_and_max_depth_of_intervals(tree)
    assert result == (0, Fraction(45, 37), 3)
