from abjad.tools.treetools import BoundedInterval
from abjad.tools.treetools import IntervalTree
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_IntervalTree_bounds_01( ):
   tree = IntervalTree([ ])
   assert tree.bounds is None


def test_IntervalTree_bounds_02( ):
   tree = IntervalTree(_make_test_blocks( ))
   assert tree.bounds == BoundedInterval(0, 37)
