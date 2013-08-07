# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_compute_logical_not_01():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    logical_not = tree.compute_logical_not()
    target_signatures = [(3, 5), (13, 15), (23, 25), (30, 32)]
    actual_signatures = [interval.signature for interval in logical_not]
    assert actual_signatures == target_signatures


def test_TimeIntervalTree_compute_logical_not_02():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.TimeInterval(5, 10))
    logical_not = tree.compute_logical_not()
    assert not len(logical_not)


def test_TimeIntervalTree_compute_logical_not_03():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(1, 14)
    logical_not = tree.compute_logical_not(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_not] == [(3, 6)]


def test_TimeIntervalTree_compute_logical_not_04():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(-1, 16)
    logical_not = tree.compute_logical_not(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_not] == [(-1, 0), (3, 6), (15, 16)]


def test_TimeIntervalTree_compute_logical_not_05():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(2001, 2010)
    logical_not = tree.compute_logical_not(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_not] == [(2001, 2010)]
