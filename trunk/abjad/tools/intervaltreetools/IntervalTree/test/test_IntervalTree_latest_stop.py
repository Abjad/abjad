from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_latest_stop_01():
    '''latest_stop returns maximum stop value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.latest_stop == 37

def test_IntervalTree_latest_stop_02():
    '''latest_stop returns None if no intervals in tree.'''
    tree = IntervalTree([])
    assert tree.latest_stop is None
