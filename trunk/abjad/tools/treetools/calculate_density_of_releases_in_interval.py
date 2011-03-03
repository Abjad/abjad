from fractions import Fraction
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def calculate_density_of_releases_in_interval(intervals, interval):
   '''Return a Fraction of the number of releases in `interval`
   divided by the magnitude of `interval`.
   '''

   assert all_are_intervals_or_trees_or_empty(intervals)
   assert isinstance(interval, BoundedInterval)
   tree = IntervalTree(intervals)

   return len(tree.find_intervals_stopping_within_interval(interval)) \
      / interval.magnitude
