import py.test
from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_fuse_tangent_or_overlapping_intervals_01( ):
   tree = IntervalTree(_make_test_blocks( ))
   fused_tree = fuse_tangent_or_overlapping_intervals(tree)
   target_signatures = [(0, 3), (5, 13), (15, 23), (25, 30), (32, 37)] 
   actual_signatures = [interval.signature for interval in fused_tree] 
   assert target_signatures == actual_signatures
   assert tree.magnitude == fused_tree.magnitude

