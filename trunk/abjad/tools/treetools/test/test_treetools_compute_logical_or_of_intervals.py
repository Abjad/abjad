import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_compute_logical_or_of_intervals_01( ):
   tree = IntervalTree(_make_test_blocks( ))
   logical_or = compute_logical_or_of_intervals(tree)
   target_signatures = [(0, 3), (5, 13), (15, 23), (25, 30), (32, 37)]
   actual_signatures = [interval.signature for interval in logical_or]
   assert actual_signatures == target_signatures

def test_treetools_compute_logical_or_of_intervals_02( ):
   tree = IntervalTree(BoundedInterval(5, 10))
   logical_or = compute_logical_or_of_intervals(tree)
   assert len(logical_or) == len(tree)
   assert logical_or[0].signature == tree[0].signature

