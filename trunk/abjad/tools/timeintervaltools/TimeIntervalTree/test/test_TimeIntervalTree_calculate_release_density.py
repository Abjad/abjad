from abjad import *


def test_TimeIntervalTree_calculate_release_density_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    release_density = tree.calculate_release_density(
        bounding_interval=timeintervaltools.TimeInterval(-2, -1))
    assert release_density == 0


def test_TimeIntervalTree_calculate_release_density_02():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    release_density = tree.calculate_release_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 37))
    assert release_density == Multiplier(12, 37)
