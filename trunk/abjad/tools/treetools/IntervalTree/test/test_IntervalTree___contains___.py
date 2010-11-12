from abjad.tools.treetools import *
from _make_test_blocks import _make_test_blocks


def test_IntervalTree___contains____01( ):
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks[0])
    assert blocks[0] in tree

def test_IntervalTree___contains____02( ): 
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks[0])
    assert blocks[1] not in tree
