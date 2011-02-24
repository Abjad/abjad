import py.test
from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_split_intervals_at_rationals_01( ):
   splits = [-1, 16]
   a = BoundedInterval(0, 10)
   b = BoundedInterval(5, 15)
   tree = IntervalTree([a, b])
   split = split_intervals_at_rationals(tree, splits)
   assert tree[:] == split[:]




