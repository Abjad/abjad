from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
import py.test


def test_intervaltreetools_compute_logical_or_of_intervals_in_interval_01():
    a = BoundedInterval(0, 3)
    b = BoundedInterval(6, 12)
    c = BoundedInterval(9, 15)
    tree = IntervalTree([a, b, c])
    d = BoundedInterval(1, 14)
    logic = compute_logical_or_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == [(1, 3), (6, 9), (9, 12), (12, 14)]

def test_intervaltreetools_compute_logical_or_of_intervals_in_interval_02():
    a = BoundedInterval(0, 3)
    b = BoundedInterval(6, 12)
    c = BoundedInterval(9, 15)
    tree = IntervalTree([a, b, c])
    d = BoundedInterval(-1, 16)
    logic = compute_logical_or_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == [(0, 3), (6, 9), (9, 12), (12, 15)]

def test_intervaltreetools_compute_logical_or_of_intervals_in_interval_03():
    a = BoundedInterval(0, 3)
    b = BoundedInterval(6, 12)
    c = BoundedInterval(9, 15)
    tree = IntervalTree([a, b, c])
    d = BoundedInterval(2001, 2010)
    logic = compute_logical_or_of_intervals_in_interval(tree, d)
    assert [x.signature for x in logic] == []
