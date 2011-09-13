from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_low_min_01():
    '''low_min returns minimum low value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.low_min == 0

def test_IntervalTree_low_min_02():
    '''low_min returns None if no intervals in tree.'''
    tree = IntervalTree([])
    assert tree.low_min is None
