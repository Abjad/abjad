from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def shift_aggregate_offset_by_rational(intervals, rational):

   assert isinstance(rational, (int, Fraction))
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree or rational == 0:
      return tree

   return IntervalTree([
      x.shift_by_rational(rational) for x in tree
   ])
