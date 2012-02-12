from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_earliest_stop_01():
    '''earliest_stop returns minimum stop value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.earliest_stop == 3

def test_IntervalTree_earliest_stop_02():
    '''earliest_stop returns None if no intervals in tree.'''
    tree = IntervalTree([])
    assert tree.earliest_stop is None
