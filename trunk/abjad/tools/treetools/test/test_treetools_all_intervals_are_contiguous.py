from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks
import py.test


def test_treetools_all_intervals_are_contiguous_01( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(10, 20)
   c = BoundedInterval(20, 30)
   tree = IntervalTree([a, b, c])
   assert all_intervals_are_contiguous(tree)

def test_treetools_all_intervals_are_contiguous_02( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(5, 15)
   tree = IntervalTree([a, b])
   assert not all_intervals_are_contiguous(tree)

def test_treetools_all_intervals_are_contiguous_03( ):
   a = BoundedInterval(0, 10)
   b = BoundedInterval(15, 25)
   tree = IntervalTree([a, b])
   assert not all_intervals_are_contiguous(tree)
