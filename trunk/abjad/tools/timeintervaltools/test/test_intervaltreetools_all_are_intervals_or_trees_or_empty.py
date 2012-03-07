from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_01():
    tree = TimeIntervalTree([])
    assert all_are_intervals_or_trees_or_empty(tree)


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_02():
    interval = TimeInterval(0, 10)
    assert all_are_intervals_or_trees_or_empty(interval)


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_03():
    tree = TimeIntervalTree([])
    other_tree = TimeIntervalTree([TimeInterval(2001, 2010)])
    interval = TimeInterval(0, 10)
    assert all_are_intervals_or_trees_or_empty([tree, other_tree, interval])


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_04():
    tree = TimeIntervalTree([])
    other_tree = TimeIntervalTree([TimeInterval(2001, 2010)])
    interval = TimeInterval(0, 10)
    assert all_are_intervals_or_trees_or_empty([tree, [[other_tree], interval], []])


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_05():
    tree = TimeIntervalTree([])
    other_tree = TimeIntervalTree([TimeInterval(2001, 2010)])
    interval = TimeInterval(0, 10)
    assert all_are_intervals_or_trees_or_empty([tree, [[other_tree], interval], [], [[interval]]])


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_06():
    tree = TimeIntervalTree([])
    other_tree = TimeIntervalTree([TimeInterval(2001, 2010)])
    interval = TimeInterval(0, 10)
    assert not all_are_intervals_or_trees_or_empty([tree, [[other_tree], interval], [], [2]])


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_07():
    assert all_are_intervals_or_trees_or_empty([])


def test_timeintervaltools_all_are_intervals_or_trees_or_empty_08():
    intervals = _make_test_intervals()
    assert all_are_intervals_or_trees_or_empty(intervals)
