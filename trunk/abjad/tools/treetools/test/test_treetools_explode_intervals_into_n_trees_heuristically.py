from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_explode_intervals_into_n_trees_heuristically_01( ):
   tree = IntervalTree(_make_test_blocks( ))
   n = 1
   result = explode_intervals_into_n_trees_heuristically(tree, n)
   assert result == \
   [IntervalTree([ \
      BoundedInterval(0, 3, 'a'), \
      BoundedInterval(5, 13, 'b'), \
      BoundedInterval(6, 10, 'c'), \
      BoundedInterval(8, 9, 'd'), \
      BoundedInterval(15, 23, 'e'), \
      BoundedInterval(16, 21, 'f'), \
      BoundedInterval(17, 19, 'g'), \
      BoundedInterval(19, 20, 'h'), \
      BoundedInterval(25, 30, 'i'), \
      BoundedInterval(26, 29, 'j'), \
      BoundedInterval(32, 34, 'k'), \
      BoundedInterval(34, 37, 'l') \
   ])]
   if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
      assert all([all_intervals_are_nonoverlapping(x) for x in result])

def test_treetools_explode_intervals_into_n_trees_heuristically_02( ):
   tree = IntervalTree(_make_test_blocks( ))
   n = 2
   result = explode_intervals_into_n_trees_heuristically(tree, n)
   assert result == \
   [IntervalTree([
      BoundedInterval(0, 3, 'a'),
      BoundedInterval(6, 10, 'c'),
      BoundedInterval(8, 9, 'd'),
      BoundedInterval(15, 23, 'e'),
      BoundedInterval(17, 19, 'g'),
      BoundedInterval(19, 20, 'h'),
      BoundedInterval(26, 29, 'j')
   ]), IntervalTree([
      BoundedInterval(5, 13, 'b'),
      BoundedInterval(16, 21, 'f'),
      BoundedInterval(25, 30, 'i'),
      BoundedInterval(32, 34, 'k'),
      BoundedInterval(34, 37, 'l')
   ])]
   if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
      assert all([all_intervals_are_nonoverlapping(x) for x in result])


def test_treetools_explode_intervals_into_n_trees_heuristically_03( ):
   tree = IntervalTree(_make_test_blocks( ))
   n = 3
   result = explode_intervals_into_n_trees_heuristically(tree, n)
   assert result == \
   [IntervalTree([
      BoundedInterval(0, 3, 'a'),
      BoundedInterval(8, 9, 'd'),
      BoundedInterval(15, 23, 'e'),
      BoundedInterval(32, 34, 'k'),
      BoundedInterval(34, 37, 'l')
   ]), IntervalTree([
      BoundedInterval(5, 13, 'b'),
      BoundedInterval(17, 19, 'g'),
      BoundedInterval(19, 20, 'h'),
      BoundedInterval(26, 29, 'j')
   ]), IntervalTree([
      BoundedInterval(6, 10, 'c'),
      BoundedInterval(16, 21, 'f'),
      BoundedInterval(25, 30, 'i')
   ])]
   if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
      assert all([all_intervals_are_nonoverlapping(x) for x in result])
