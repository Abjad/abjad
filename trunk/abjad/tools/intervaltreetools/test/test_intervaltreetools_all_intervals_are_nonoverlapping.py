from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
import py.test


def test_intervaltreetools_all_intervals_are_nonoverlapping_01():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(10, 20)
    tree = IntervalTree([a, b])
    assert all_intervals_are_nonoverlapping(tree)

def test_intervaltreetools_all_intervals_are_nonoverlapping_02():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    tree = IntervalTree([a, b])
    assert not all_intervals_are_nonoverlapping(tree)

def test_intervaltreetools_all_intervals_are_nonoverlapping_03():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(15, 25)
    tree = IntervalTree([a, b])
    assert all_intervals_are_nonoverlapping(tree)
