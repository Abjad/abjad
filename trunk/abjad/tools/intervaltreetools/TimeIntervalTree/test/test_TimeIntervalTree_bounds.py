from abjad.tools.intervaltreetools import TimeInterval
from abjad.tools.intervaltreetools import TimeIntervalTree
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree_bounds_01():
    tree = TimeIntervalTree([])
    assert tree.bounds is None


def test_TimeIntervalTree_bounds_02():
    tree = TimeIntervalTree(_make_test_intervals())
    assert tree.bounds == TimeInterval(0, 37)
