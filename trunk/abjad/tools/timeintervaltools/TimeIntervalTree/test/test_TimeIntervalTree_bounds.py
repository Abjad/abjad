import py.test
from abjad.tools.timeintervaltools import TimeInterval
from abjad.tools.timeintervaltools import TimeIntervalTree
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree_bounds_01():
    tree = TimeIntervalTree([])
    py.test.raises(Exception, 'tree.bounds')

def test_TimeIntervalTree_bounds_02():
    tree = TimeIntervalTree(_make_test_intervals())
    assert tree.bounds == TimeInterval(0, 37)
