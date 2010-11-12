from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_IntervalTree_insert_01( ):
    '''A single interval can be inserted into a tree.'''
    blocks = _make_test_blocks( )
    tree = IntervalTree( )
    for block in blocks:
        tree.insert(block)
        assert block in tree

def test_IntervalTree_insert_02( ):
    '''Lists of intervals can be inserted into a tree.'''
    blocks = _make_test_blocks( )
    tree = IntervalTree( )
    tree.insert(blocks)
    for block in blocks:
        assert block in tree

def test_IntervalTree_insert_03( ):
    '''Intervals with identical signatures can be inserted into a tree.'''
    blocks = _make_test_blocks( )
    tree = IntervalTree( )
    a = blocks[0]
    b = Block(a)
    assert a != b and a.signature == b.signature
    tree.insert([a, b])
    assert a in tree and b in tree
