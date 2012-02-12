from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree_latest_start_01():
    '''latest_start returns maximum start value of all intervals in tree.'''
    blocks = _make_test_intervals()
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.latest_start == 34

def test_IntervalTree_latest_start_02():
    '''latest_start returns None if no intervals in tree.'''
    tree = IntervalTree([])
    assert tree.latest_start is None
