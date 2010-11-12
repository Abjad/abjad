from abjad.tools.treetools import *
from _make_test_blocks import _make_test_blocks


def test_IntervalTree_inorder_01( ):
    blocks = _make_test_blocks( )
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0))
        tree = IntervalTree(blocks)
        assert tuple(sorted(blocks, key=lambda x: x.signature)) \
            == tree.inorder

