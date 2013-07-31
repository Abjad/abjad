# -*- encoding: utf-8 -*-
from abjad import *


def test_TimeIntervalTree_calculate_depth_density_01():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    c = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(-10, -5)) == 0


def test_TimeIntervalTree_calculate_depth_density_02():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    c = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(30, 40)) == 0


def test_TimeIntervalTree_calculate_depth_density_03():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    c = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 5)) == 1


def test_TimeIntervalTree_calculate_depth_density_04():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    c = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 10)) == \
        Multiplier(3, 2)


def test_TimeIntervalTree_calculate_depth_density_05():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    c = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 15)) == \
        Multiplier(4, 3)


def test_TimeIntervalTree_calculate_depth_density_06():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    c = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 20)) == 1


def test_TimeIntervalTree_calculate_depth_density_07():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    c = timeintervaltools.TimeInterval(20, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.calculate_depth_density(
        bounding_interval=timeintervaltools.TimeInterval(0, 25)) == 1
