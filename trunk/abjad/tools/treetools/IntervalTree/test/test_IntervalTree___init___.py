from abjad.tools.treetools import *


def test_IntervalTree___init____01( ):
    '''IntervalTree can be initialized without arguments.'''
    tree = IntervalTree( )


def test_IntervalTree___init___02( ):
    '''IntervalTree can be initialized from a list of Blocks.'''
    block_a = Block(0, 10, 'a')
    block_b = Block(5, 15, 'b')
    block_c = Block(10, 5, 'c')
    tree = IntervalTree([block_a, block_b, block_c])
