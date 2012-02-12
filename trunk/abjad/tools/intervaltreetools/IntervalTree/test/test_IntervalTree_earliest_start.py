from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_earliest_start_01():
    '''earliest_start returns minimum start value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.earliest_start == 0

def test_IntervalTree_earliest_start_02():
    '''earliest_start returns None if no intervals in tree.'''
    tree = IntervalTree([])
    assert tree.earliest_start is None
