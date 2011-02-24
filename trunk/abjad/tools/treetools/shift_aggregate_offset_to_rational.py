from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def shift_aggregate_offset_to_rational(intervals, rational):

   assert isinstance(rational, (int, Fraction))
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree or rational == tree.low:
      return tree

   shift = rational - tree.low

   return IntervalTree([
      x.shift_by_rational(rational - tree.low) for x in tree
   ])
