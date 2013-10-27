# -*- encoding: utf-8 -*-
from abjad import *


def test_timeintervaltools_TimeIntervalTree_calculate_depth_density_01():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    time_interval_3 = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(-10, -5)) == 0


def test_timeintervaltools_TimeIntervalTree_calculate_depth_density_02():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    time_interval_3 = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(30, 40)) == 0


def test_timeintervaltools_TimeIntervalTree_calculate_depth_density_03():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    time_interval_3 = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 5)) == 1


def test_timeintervaltools_TimeIntervalTree_calculate_depth_density_04():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    time_interval_3 = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 10)) == \
        Multiplier(3, 2)


def test_timeintervaltools_TimeIntervalTree_calculate_depth_density_05():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    time_interval_3 = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 15)) == \
        Multiplier(4, 3)


def test_timeintervaltools_TimeIntervalTree_calculate_depth_density_06():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    time_interval_3 = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 20)) == 1


def test_timeintervaltools_TimeIntervalTree_calculate_depth_density_07():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    time_interval_3 = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 25)) == 1
