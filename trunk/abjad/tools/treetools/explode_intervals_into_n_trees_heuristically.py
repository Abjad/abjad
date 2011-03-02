from fractions import Fraction
from abjad.tools.treetools import *


def explode_intervals_into_n_trees_minimizing_overlap(intervals, n):
# create n trees
# add an interval to one tree
# for each interval
#   find those trees where there is no overlap
#   add it to the tree with least density
# if all trees have overlap
#   find tree with least overlap
# if overlaps are tied
#   choose least dense overlapping tree
# else
#   just add it to first in tie

   assert all_are_intervals_or_trees_or_empty(intervals)
   assert isinstance(n, int) and 0 < n
   tree = IntervalTree(intervals)

   trees = IntervalTree([ ]) * n

   if not tree:
      return trees

   trees[0] = IntervalTree([tree[0]])
   for interval in tree[1:]:
      nonoverlapping_trees = [ ]
      overlapping_trees = [ ]

      for t in trees:
         if not len(t):
            nonoverlapping_trees.append(t)
         elif not t[-1].is_overlapped_by_interval(interval):
            nonoverlapping_trees.append(t)
         else:
            overlapping_trees.append(t)

      if len(nonoverlapping_trees):
         # sort by least dense
         sort(nonoverlapping_trees, key = lambda x: \
            compute_depth_density_of_intervals_in_interval(t, \
               BoundedInterval(tree.low, tree.high)))
         match_id = trees.index(nonoverlapping_trees[0])
         trees[match_id] = IntervalTree([trees[match_id], interval])

      else:
         # first, sort by least overlap with current interval
         sort(overlapping_trees, key = lambda x: \
            x[-1].get_overlap_with_interval(interval))

         # test for tie

         # if no tie, add to least overlap


         # else add to least dense of tie
         sort(overlapping_trees, key = lambda x: \
            compute_depth_density_of_intervals_in_interval(t, \
               BoundedInterval(tree.low, tree.high)))
