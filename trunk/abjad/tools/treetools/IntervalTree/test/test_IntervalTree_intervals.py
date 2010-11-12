import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_IntervalTree_intervals_01( ):
    '''intervals returns a tuple of all intervals in the tree,
       in the order they were inserted.'''
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks)
    assert tuple(blocks) == tree.intervals

def test_IntervalTree_intervals_02( ):
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks)
    blocks.append(blocks.pop(0))
    assert tuple(blocks) != tree.intervals
