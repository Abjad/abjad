import py.test
from random import shuffle
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks

#py.test.skip('Awaiting rewrite of IntervalTree backend.')

def test_IntervalTree_remove_01( ):
    '''A single interval can be removed from a tree.'''
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks)
    assert blocks[0] in tree        
    tree.remove(blocks[0])
    assert blocks[0] not in tree

def test_IntervalTree_remove_02( ):
    '''Multiple intervals can be removed from a tree at once.'''
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks)
    for block in blocks:
        assert block in tree
    tree.remove(tree.intervals)
    for block in blocks:
        assert block not in tree

def test_IntervalTree_remove_03( ):
    '''Non-member intervals cannot be removed from a tree.'''
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks[1:])
    for block in blocks[1:]:
        assert block in tree
    py.test.raises(AssertionError,
        'tree.remove(blocks[0])')

def test_IntervalTree_remove_04( ):
    '''Intervals can be removed regardless of the tree's internal structure.'''
    py.test.skip('test intermittently fails and should be fixed.')
    blocks = _make_test_blocks( )
    for i in range(100):
        shuffle(blocks)
        tree = IntervalTree(blocks)
        assert len(tree) == len(blocks)
        shuffle(blocks)
        count = len(tree)
        starting_length = count
        for j in range(starting_length):
            tree.remove(blocks[j])
            count -= 1
            assert len(tree) == count
            assert blocks[j] not in tree
            
