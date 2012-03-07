from abjad.tools.intervaltreetools import TimeInterval
from abjad.tools.intervaltreetools import IntervalTree
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_bounds_01():
    tree = IntervalTree([])
    assert tree.bounds is None


def test_IntervalTree_bounds_02():
    tree = IntervalTree(_make_test_intervals())
    assert tree.bounds == TimeInterval(0, 37)
