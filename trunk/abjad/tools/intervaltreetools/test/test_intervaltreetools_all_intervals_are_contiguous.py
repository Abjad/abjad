from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
import py.test


def test_intervaltreetools_all_intervals_are_contiguous_01():
    a = TimeInterval(0, 10)
    b = TimeInterval(10, 20)
    c = TimeInterval(20, 30)
    tree = IntervalTree([a, b, c])
    assert all_intervals_are_contiguous(tree)

def test_intervaltreetools_all_intervals_are_contiguous_02():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    tree = IntervalTree([a, b])
    assert not all_intervals_are_contiguous(tree)

def test_intervaltreetools_all_intervals_are_contiguous_03():
    a = TimeInterval(0, 10)
    b = TimeInterval(15, 25)
    tree = IntervalTree([a, b])
    assert not all_intervals_are_contiguous(tree)
