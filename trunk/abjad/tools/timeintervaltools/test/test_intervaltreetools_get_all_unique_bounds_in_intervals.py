from abjad.tools.timeintervaltools import get_all_unique_bounds_in_intervals
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_timeintervaltools_get_all_unique_bounds_in_intervals_01():
    tree = TimeIntervalTree(_make_test_intervals())
    target_bounds = (0, 3, 5, 6, 8, 9, 10, 13, 15, 16, 17, 19, 20, 21, 23, 25, 26, 29, 30, 32, 34, 37)
    actual_bounds = get_all_unique_bounds_in_intervals(tree)
    assert actual_bounds == target_bounds


def test_timeintervaltools_get_all_unique_bounds_in_intervals_02():
    tree = TimeIntervalTree([])
    target_bounds = ()
    actual_bounds = get_all_unique_bounds_in_intervals(tree)
    assert actual_bounds == target_bounds
