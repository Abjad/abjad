import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


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

#def test_IntervalTree_remove_04( ):
#    '''Intervals can be removed regardless of the tree's internal structure.'''
#    blocks = _make_test_blocks( )
#    lenblocks = len(blocks)
#    for i in range(lenblocks):
#        blocks = _make_test_blocks( )
#        for j in range(i):
#            blocks.append(blocks.pop(0))
#        tree = IntervalTree(blocks)
#        for j in range(lenblocks):
#            tree.remove(tree.intervals[0])

#def test_IntervalTree_remove_04( ):
#    '''Intervals can be removed regardless of the tree's internal structure.'''
#    from random import shuffle
#    for i in range(100):
#        blocks = _make_test_blocks( )
#        shuffle(blocks)
#        tree = IntervalTree(blocks)
#        for block in blocks:
#            tree.remove(block)
#            assert block not in tree  
