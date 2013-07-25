from abjad import *


def test_TimeIntervalTree_calculate_depth_centroid_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    depth_centroid = tree.calculate_depth_centroid(
        bounding_interval=timeintervaltools.TimeInterval(0, 10))
    assert depth_centroid == Multiplier(131, 18)


def test_TimeIntervalTree_calculate_depth_centroid_02():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    depth_centroid = tree.calculate_depth_centroid(
        bounding_interval=timeintervaltools.TimeInterval(-100, -10))
    assert depth_centroid is None
