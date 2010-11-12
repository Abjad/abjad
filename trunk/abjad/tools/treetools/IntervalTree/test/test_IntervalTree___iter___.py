from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_IntervalTree___iter____01( ):
    blocks = _make_test_blocks( )
    tree = IntervalTree(blocks)
    for e in enumerate(tree.intervals):
        assert blocks[e[0]] == e[1]    
