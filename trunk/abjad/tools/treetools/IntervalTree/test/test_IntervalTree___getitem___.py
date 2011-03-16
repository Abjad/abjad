from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_IntervalTree___getitem____01( ):
   intervals = _make_test_blocks( )
   tree = IntervalTree(intervals)
   assert tree[0] == intervals[0]
   assert tree[1] == intervals[1]
   assert tree[-1] == intervals[-1]
   assert tree[-2] == intervals[-2]
