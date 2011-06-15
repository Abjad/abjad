from abjad import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks
import py.test


def test_treetools_calculate_density_of_releases_in_interval_01( ):
   tree = IntervalTree(_make_test_blocks( ))
   assert calculate_density_of_releases_in_interval(tree,
      BoundedInterval(-2, -1)) == 0


def test_treetools_calculate_density_of_releases_in_interval_02( ):
   tree = IntervalTree(_make_test_blocks( ))
   assert calculate_density_of_releases_in_interval(tree,
      BoundedInterval(0, 37)) == Fraction(12, 37)
