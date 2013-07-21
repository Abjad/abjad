from abjad import *
import py.test


def test_timeintervaltools_compute_logical_or_of_intervals_in_interval_01():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(1, 14)
    logic = timeintervaltools.compute_logical_or_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == [(1, 3), (6, 9), (9, 12), (12, 14)]


def test_timeintervaltools_compute_logical_or_of_intervals_in_interval_02():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(-1, 16)
    logic = timeintervaltools.compute_logical_or_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == [(0, 3), (6, 9), (9, 12), (12, 15)]


def test_timeintervaltools_compute_logical_or_of_intervals_in_interval_03():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(2001, 2010)
    logic = timeintervaltools.compute_logical_or_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == []
