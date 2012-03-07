from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
import py.test


def test_timeintervaltools_all_intervals_are_nonoverlapping_01():
    a = TimeInterval(0, 10)
    b = TimeInterval(10, 20)
    tree = TimeIntervalTree([a, b])
    assert all_intervals_are_nonoverlapping(tree)

def test_timeintervaltools_all_intervals_are_nonoverlapping_02():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    tree = TimeIntervalTree([a, b])
    assert not all_intervals_are_nonoverlapping(tree)

def test_timeintervaltools_all_intervals_are_nonoverlapping_03():
    a = TimeInterval(0, 10)
    b = TimeInterval(15, 25)
    tree = TimeIntervalTree([a, b])
    assert all_intervals_are_nonoverlapping(tree)
