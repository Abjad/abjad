from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
import py.test


def test_timeintervaltools_compute_logical_xor_of_intervals_in_interval_01():
    a = TimeInterval(0, 3)
    b = TimeInterval(6, 12)
    c = TimeInterval(9, 15)
    tree = TimeIntervalTree([a, b, c])
    d = TimeInterval(1, 14)
    logic = compute_logical_xor_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == [(1, 3), (6, 9), (12, 14)]

def test_timeintervaltools_compute_logical_xor_of_intervals_in_interval_02():
    a = TimeInterval(0, 3)
    b = TimeInterval(6, 12)
    c = TimeInterval(9, 15)
    tree = TimeIntervalTree([a, b, c])
    d = TimeInterval(-1, 16)
    logic = compute_logical_xor_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == [(0, 3), (6, 9), (12, 15)]

def test_timeintervaltools_compute_logical_xor_of_intervals_in_interval_03():
    a = TimeInterval(0, 3)
    b = TimeInterval(6, 12)
    c = TimeInterval(9, 15)
    tree = TimeIntervalTree([a, b, c])
    d = TimeInterval(2001, 2010)
    logic = compute_logical_xor_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == []
