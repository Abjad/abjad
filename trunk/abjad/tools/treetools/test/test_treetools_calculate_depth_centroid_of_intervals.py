from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_calculate_depth_centroid_of_intervals_01( ):
   tree = IntervalTree(_make_test_blocks( ))
   result = calculate_depth_centroid_of_intervals(tree)
   assert result == Fraction(137, 8)


def test_treetools_calculate_depth_centroid_of_intervals_02( ):
   tree = IntervalTree([ ])
   result = calculate_depth_centroid_of_intervals(tree)
   assert result is None
