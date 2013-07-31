# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_compute_logical_and_01():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    logical_and = tree.compute_logical_and()
    target_signatures = [(6, 8), (8, 9), (9, 10), (16, 17),
        (17, 19), (19, 20), (20, 21), (26, 29)]
    actual_signatures = [interval.signature for interval in logical_and]
    assert actual_signatures == target_signatures


def test_TimeIntervalTree_compute_logical_and_02():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.TimeInterval(5, 10))
    logical_and = tree.compute_logical_and()
    assert not len(logical_and)


def test_TimeIntervalTree_compute_logical_and_03():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(1, 14)
    logical_and = tree.compute_logical_and(bounding_interval=d)
    assert [x.signature for x in logical_and] == [(9, 12)]


def test_TimeIntervalTree_compute_logical_and_04():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(-1, 16)
    logical_and = tree.compute_logical_and(bounding_interval=d)
    assert [x.signature for x in logical_and] == [(9, 12)]


def test_TimeIntervalTree_compute_logical_and_05():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(2001, 2010)
    logical_and = tree.compute_logical_and(bounding_interval=d)
    assert [x.signature for x in logical_and] == []
