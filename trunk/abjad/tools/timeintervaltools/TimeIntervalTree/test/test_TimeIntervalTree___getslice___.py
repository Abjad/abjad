from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree___getslice____01():
    intervals = _make_test_intervals()
    tree = TimeIntervalTree(intervals)
    assert tuple(intervals[:]) == tree[:]
    assert tuple(intervals[:2]) == tree[:2]
    assert tuple(intervals[-2:]) == tree[-2:]
    assert tuple(intervals[1:3]) == tree[1:3]
