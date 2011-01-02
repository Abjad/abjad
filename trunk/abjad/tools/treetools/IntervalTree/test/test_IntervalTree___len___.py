from abjad.tools.treetools import *


def test_IntervalTree___len____01( ):
    '''IntervalTree containing no Blocks report 0 length.'''
    tree = IntervalTree([ ])
    assert len(tree) == 0


def test_IntervalTree___len____02( ):
    '''IntervalTree reports total count of Blocks contained.'''
    block_a = Block(0, 5, 'a')
    block_b = Block(0, 10, 'b')
    block_c = Block(5, 20, 'c')
    tree = IntervalTree([block_a, block_b, block_c])
    assert len(tree) == 3
