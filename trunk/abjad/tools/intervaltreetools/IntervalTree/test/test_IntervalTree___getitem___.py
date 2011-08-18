from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree___getitem____01():
    intervals = _make_test_intervals()
    tree = IntervalTree(intervals)
    assert tree[0] == intervals[0]
    assert tree[1] == intervals[1]
    assert tree[-1] == intervals[-1]
    assert tree[-2] == intervals[-2]
