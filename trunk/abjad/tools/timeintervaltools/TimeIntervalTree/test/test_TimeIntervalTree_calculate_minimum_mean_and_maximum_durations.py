from abjad import *


def test_TimeIntervalTree_calculate_minimum_mean_and_maximum_durations_01():
    tree = timeintervaltools.TimeIntervalTree([])
    result = tree.calculate_minimum_mean_and_maximum_durations()
    assert result is None


def test_TimeIntervalTree_calculate_minimum_mean_and_maximum_durations_02():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    result = tree.calculate_minimum_mean_and_maximum_durations()
    assert result == (1, Multiplier(15, 4), 8)
