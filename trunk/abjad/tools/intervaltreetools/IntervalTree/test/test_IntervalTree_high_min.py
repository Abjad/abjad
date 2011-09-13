from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_high_min_01():
    '''high_min returns minimum high value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.high_min == 3

def test_IntervalTree_high_min_02():
    '''high_min returns None if no intervals in tree.'''
    tree = IntervalTree([])
    assert tree.high_min is None
