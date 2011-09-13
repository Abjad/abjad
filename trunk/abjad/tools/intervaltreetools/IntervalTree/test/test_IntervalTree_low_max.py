from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_low_max_01():
    '''low_max returns maximum low value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.low_max == 34

def test_IntervalTree_low_max_02():
    '''low_max returns None if no intervals in tree.'''
    tree = IntervalTree([])
    assert tree.low_max is None
