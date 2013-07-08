from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_calculate_depth_centroid_of_intervals_in_interval_01():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    interval = TimeInterval(0, 10)
    depth_centroid = calculate_depth_centroid_of_intervals_in_interval(
        tree, interval)
    assert depth_centroid == Fraction(131, 18)


def test_timeintervaltools_calculate_depth_centroid_of_intervals_in_interval_02():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    interval = TimeInterval(-100, -10)
    depth_centroid = calculate_depth_centroid_of_intervals_in_interval(
        tree, interval)
    assert depth_centroid is None
