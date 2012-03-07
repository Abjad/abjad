from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree_earliest_stop_01():
    '''earliest_stop returns minimum stop value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = TimeIntervalTree(blocks)
        assert tree.earliest_stop == 3

def test_TimeIntervalTree_earliest_stop_02():
    '''earliest_stop returns None if no intervals in tree.'''
    tree = TimeIntervalTree([])
    assert tree.earliest_stop is None
