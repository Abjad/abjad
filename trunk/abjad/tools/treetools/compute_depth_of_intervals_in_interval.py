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
   tree = IntervalTree(intervals)

   bounds = list(get_all_unique_bounds_in_intervals(tree))
   bounds.extend([interval.low, interval.high])
   bounds = sorted(list(set(bounds)))

   tree = split_intervals_at_rationals(tree, bounds)
   tree = IntervalTree(tree.find_intervals_starting_and_stopping_within_interval(interval.low, interval.high))

   bounds = list(get_all_unique_bounds_in_intervals(tree))
   bounds.extend([interval.low, interval.high])
   bounds = sorted(list(set(bounds)))

   intervals = [ ]
   for i in range(len(bounds) - 1):
      s, e = bounds[i], bounds[i + 1]
      count = len(tree.find_intervals_starting_and_stopping_within_interval(s, e))
      intervals.append(BoundedInterval(s, e, {'depth': count}))

   return IntervalTree(intervals)
