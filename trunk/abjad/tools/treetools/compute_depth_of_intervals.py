from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty
from abjad.tools.treetools.get_all_unique_bounds_in_intervals \
   import get_all_unique_bounds_in_intervals


def compute_depth_of_intervals(intervals):
   '''Compute a tree whose intervals represent the depth (level of overlap) 
   in each boundary pair of `tree`::
      abjad> from abjad.tools.treetools import *
      abjad> tree = IntervalTree([ ])
      abjad> tree.insert(BoundedInterval(0, 3))
      abjad> tree.insert(BoundedInterval(6, 12))
      abjad> tree.insert(BoundedInterval(9, 15))
      abjad> compute_depth_of_intervals(tree)
      IntervalTree([
         BoundedInterval(0, 3, data = {'depth': 1}),
         BoundedInterval(3, 6, data = {'depth': 0}),
         BoundedInterval(6, 9, data = {'depth': 1}),
         BoundedInterval(9, 12, data = {'depth': 2}),
         BoundedInterval(12, 15, data = {'depth': 1})
      ])
   '''

   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)

   values = get_all_unique_bounds_in_intervals(tree)
   intervals = [ ]
   for i in range(len(values[1:])):
      found_a = set(tree.find_intervals_intersecting_or_tangent_to_interval(values[i], values[i + 1]))
      found_b = set(tree.find_intervals_starting_at_offset(values[i + 1]))
      found_c = set(tree.find_intervals_stopping_at_offset(values[i]))
      found = found_a.difference(found_b)
      found = tuple(found.difference(found_c))
      zeros = filter(lambda x: x.low == x.high, found_c)
      if zeros:
         intervals.append(BoundedInterval(values[i], values[i], {'depth': len(found) + len(zeros)}))
      intervals.append(BoundedInterval(values[i], values[i + 1], {'depth': len(found)}))
   return IntervalTree(intervals)
