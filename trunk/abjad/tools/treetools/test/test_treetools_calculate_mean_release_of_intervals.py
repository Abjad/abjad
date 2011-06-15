from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks
from abjad import Fraction


def test_treetools_calculate_mean_release_of_intervals_01( ):
   tree = IntervalTree(_make_test_blocks( ))
   release = calculate_mean_release_of_intervals(tree)
   assert release == Fraction(sum([x.high for x in tree]), len(tree))


def test_treetools_calculate_mean_release_of_intervals_02( ):
   tree = IntervalTree([ ])
   release = calculate_mean_release_of_intervals(tree)
   assert release is None

