from fractions import Fraction
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty
from abjad.tools.treetools.calculate_depth_density_of_intervals_in_interval \
   import calculate_depth_density_of_intervals_in_interval


def explode_intervals_into_n_trees_heuristically(intervals, n):
   '''Explode `intervals` into `n` trees, avoiding overlap when possible,
   and distributing intervals so as to equalize density across the trees.
   '''

   assert all_are_intervals_or_trees_or_empty(intervals)
   assert isinstance(n, int) and 0 < n
   tree = IntervalTree(intervals)

   trees = [IntervalTree([ ])] * n

   if not tree:
      return trees

   trees[0] = IntervalTree([tree[0]])
   for interval in tree[1:]:
      nonoverlapping_trees = [ ]
      overlapping_trees = [ ]

      # sort trees into overlapping and non-overlapping groups
      for t in trees:
         if not len(t):
            nonoverlapping_trees.append(t)
         elif not t[-1].is_overlapped_by_interval(interval):
            nonoverlapping_trees.append(t)
         else:
            overlapping_trees.append(t)

      # if there are any non-overlapping trees, choose the least dense
      if len(nonoverlapping_trees):
         # sort by least dense
         sorted(nonoverlapping_trees, key = lambda x: \
            calculate_depth_density_of_intervals_in_interval(t, \
               BoundedInterval(tree.low, tree.high)))
         match_id = trees.index(nonoverlapping_trees[0])
         trees[match_id] = IntervalTree([trees[match_id], interval])

      # else, find the least-overlapping overlapping tree
      else:
         # first, sort by least overlap with current interval
         sorted(overlapping_trees, key = lambda x: \
            x[-1].get_overlap_with_interval(interval))

         # test for tie
         ties = filter(lambda x: x[-1].get_overlap_with_interval(interval) == \
            overlapping_trees[0][-1].get_overlap_with_interval(interval), \
            overlapping_trees)

         # if no tie, add to least overlap
         if len(ties) == 1:
            trees[trees.index(ties[0])] = IntervalTree([trees[trees.index(ties[0])], interval])

         # else add to least dense of tie
         else:
            sorted(ties, key = lambda x: \
               calculate_depth_density_of_intervals_in_interval(t, \
                  BoundedInterval(tree.low, tree.high)))
            trees[trees.index(ties[0])] = IntervalTree([trees[trees.index(ties[0])], interval])

   return trees
