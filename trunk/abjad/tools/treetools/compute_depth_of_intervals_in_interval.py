from abjad.tools.seqtools import iterate_sequence_pairwise_strict
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty
from abjad.tools.treetools.get_all_unique_bounds_in_intervals \
   import get_all_unique_bounds_in_intervals
from abjad.tools.treetools.split_intervals_at_rationals \
   import split_intervals_at_rationals


def compute_depth_of_intervals_in_interval(intervals, interval):
   '''Compute a tree whose intervals represent the depth (level of overlap) 
   in each boundary pair of `intervals`, cropped within `interval`::

      abjad> from abjad.tools.treetools import *
      abjad> a = BoundedInterval(0, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 15)
      abjad> tree = IntervalTree([a, b, c])
      abjad> d = BoundedInterval(-1, 16)
      abjad> compute_depth_of_intervals_in_interval(tree)
      IntervalTree([
         BoundedInterval(-1, 0, data = {'depth': 0}),
         BoundedInterval(0, 3, data = {'depth': 1}),
         BoundedInterval(3, 6, data = {'depth': 0}),
         BoundedInterval(6, 9, data = {'depth': 1}),
         BoundedInterval(9, 12, data = {'depth': 2}),
         BoundedInterval(12, 15, data = {'depth': 1}),
         BoundedInterval(15, 16, data = {'depth': 0})
      ])
   '''

   assert all_are_intervals_or_trees_or_empty(intervals)
   assert isinstance(interval, BoundedInterval)
   if isinstance(intervals, IntervalTree):
      tree = intervals
   else:
      tree = IntervalTree(intervals)

   if interval.high <= tree.low or tree.high <= interval.low:
      return IntervalTree([BoundedInterval(interval.low, interval.high, {'depth': 0})])
   else:
      bounds = list(get_all_unique_bounds_in_intervals(tree))
      if interval.low < tree.low:
         bounds.insert(0, interval.low)
      elif tree.low < interval.low:
         bounds = filter(lambda x: interval.low <= x, bounds)
         bounds.insert(0, interval.low)
      if tree.high < interval.high:
         bounds.append(interval.high)
      elif interval.high < tree.high:
         bounds = filter(lambda x: x <= interval.high, bounds)
         bounds.append(interval.high)
      bounds = sorted(list(set(bounds)))

   intervals = [ ]
#   for i in range(len(bounds) - 1):
   for pair in iterate_sequence_pairwise_strict(bounds):
      target = BoundedInterval(pair[0], pair[1], { })
      found = tree.find_intervals_intersecting_or_tangent_to_interval(target)
      if found:
         target.data['depth'] = len(filter( \
            lambda x: not x.low == target.high and not x.high == target.low, found))
      else:
         target.data['depth'] = 0
      intervals.append(target)

   return IntervalTree(intervals)

#   tree = split_intervals_at_rationals(tree, [interval.low, interval.high])
#   tree = IntervalTree(tree.find_intervals_starting_and_stopping_within_interval(interval.low, interval.high))
#   bounds = list(get_all_unique_bounds_in_intervals(tree))
#   if interval.low not in bounds:
#      bounds.append(interval.low)
#   if interval.high not in bounds:
#      bounds.append(interval.high)
#   bounds.sort( )
#   intervals = [ ]
#   for i in range(len(bounds) - 1):
#      target = BoundedInterval(bounds[i], bounds[i+1], { })
#      found = tree.find_intervals_intersecting_or_tangent_to_interval(target)
#      if found:
#         depth = len(filter(lambda x: not x.low == target.high and not x.high == target.low, found))
#      else:
#         depth = 0
#      target.data['depth'] = depth
#      intervals.append(target)
#   return IntervalTree(intervals)
