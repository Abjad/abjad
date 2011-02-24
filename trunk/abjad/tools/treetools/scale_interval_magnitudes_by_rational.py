from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def scale_interval_magnitudes_by_rational(intervals, rational):

   assert isinstance(rational, (int, Fraction)) and 0 < rational
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree or rational == 1:
      return tree

   return IntervalTree([
      x.scale_by_rational(rational) for x in tree
   ])
