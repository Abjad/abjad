from abjad.tools.treetools import *
from _make_test_blocks import _make_test_blocks


def test_IntervalTree_low_min_01( ):
    '''low_min returns minimum low value of all intervals in tree.'''
    blocks = _make_test_blocks( )
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tree.low_min == 0

def test_IntervalTree_low_min_02( ):
    '''low_min returns None if no intervals in tree.'''
    tree = IntervalTree( )
    assert tree.low_min is None

