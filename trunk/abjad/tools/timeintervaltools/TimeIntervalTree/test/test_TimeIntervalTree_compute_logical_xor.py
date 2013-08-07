# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_compute_logical_xor_01():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    logical_xor = tree.compute_logical_xor()
    target_signatures = [(0, 3), (5, 6), (10, 13), (15, 16), (21, 23), (25, 26), (29, 30), (32, 34), (34, 37)]
    actual_signatures = [interval.signature for interval in logical_xor]
    assert actual_signatures == target_signatures


def test_TimeIntervalTree_compute_logical_xor_02():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.TimeInterval(5, 10))
    logical_xor = tree.compute_logical_xor()
    assert len(logical_xor) == len(tree)
    assert logical_xor[0].signature == tree[0].signature


def test_TimeIntervalTree_compute_logical_xor_03():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(1, 14)
    logical_xor = tree.compute_logical_xor(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_xor] == [(1, 3), (6, 9), (12, 14)]


def test_TimeIntervalTree_compute_logical_xor_04():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(-1, 16)
    logical_xor = tree.compute_logical_xor(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_xor] == [(0, 3), (6, 9), (12, 15)]


def test_TimeIntervalTree_compute_logical_xor_05():
    time_interval_1 = timeintervaltools.TimeInterval(0, 3)
    time_interval_2 = timeintervaltools.TimeInterval(6, 12)
    time_interval_3 = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    time_interval_4 = timeintervaltools.TimeInterval(2001, 2010)
    logical_xor = tree.compute_logical_xor(bounding_interval=time_interval_4)
    assert [x.signature for x in logical_xor] == []
