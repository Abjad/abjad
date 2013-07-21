from abjad import *
import py.test


def test_timeintervaltools_compute_logical_or_of_intervals_01():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    logical_or = timeintervaltools.compute_logical_or_of_intervals(tree)
    target_signatures = [(0, 3), (5, 6), (6, 8), (8, 9), (9, 10),
        (10, 13), (15, 16), (16, 17), (17, 19),
        (19, 20), (20, 21), (21, 23), (25, 26),
        (26, 29), (29, 30), (32, 34), (34, 37)]
    actual_signatures = [interval.signature for interval in logical_or]
    assert actual_signatures == target_signatures


def test_timeintervaltools_compute_logical_or_of_intervals_02():
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.TimeInterval(5, 10))
    logical_or = timeintervaltools.compute_logical_or_of_intervals(tree)
    assert len(logical_or) == len(tree)
    assert logical_or[0].signature == tree[0].signature


def test_timeintervaltools_compute_logical_or_of_intervals_03():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(1, 14)
    logic = timeintervaltools.compute_logical_or_of_intervals(tree, d)
    assert [x.signature for x in logic] == [(1, 3), (6, 9), (9, 12), (12, 14)]


def test_timeintervaltools_compute_logical_or_of_intervals_04():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(-1, 16)
    logic = timeintervaltools.compute_logical_or_of_intervals(tree, d)
    assert [x.signature for x in logic] == [(0, 3), (6, 9), (9, 12), (12, 15)]


def test_timeintervaltools_compute_logical_or_of_intervals_05():
    a = timeintervaltools.TimeInterval(0, 3)
    b = timeintervaltools.TimeInterval(6, 12)
    c = timeintervaltools.TimeInterval(9, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    d = timeintervaltools.TimeInterval(2001, 2010)
    logic = timeintervaltools.compute_logical_or_of_intervals(tree, d)
    assert [x.signature for x in logic] == []
