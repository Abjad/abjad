# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_timeintervaltools_TimeIntervalTree_compute_logical_or_01():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    logical_or = tree.compute_logical_or()
    target_signatures = [(0, 3), (5, 6), (6, 8), (8, 9), (9, 10),
        (10, 13), (15, 16), (16, 17), (17, 19),
        (19, 20), (20, 21), (21, 23), (25, 26),
        (26, 29), (29, 30), (32, 34), (34, 37)]
    actual_signatures = [interval.signature for interval in logical_or]
    assert actual_signatures == target_signatures


def test_timeintervaltools_TimeIntervalTree_compute_logical_or_02():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.TimeInterval(5, 10))
    logical_or = tree.compute_logical_or()
    assert len(logical_or) == len(tree)
    assert logical_or[0].signature == tree[0].signature


def test_timeintervaltools_TimeIntervalTree_compute_logical_or_03():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(1, 14)
    logical_or = tree.compute_logical_or(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_or] == [(1, 3), (6, 9), (9, 12), (12, 14)]


def test_timeintervaltools_TimeIntervalTree_compute_logical_or_04():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(-1, 16)
    logical_or = tree.compute_logical_or(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_or] == [(0, 3), (6, 9), (9, 12), (12, 15)]


def test_timeintervaltools_TimeIntervalTree_compute_logical_or_05():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(2001, 2010)
    logical_or = tree.compute_logical_or(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_or] == []
