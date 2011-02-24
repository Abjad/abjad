from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def scale_aggregate_magnitude_to_rational(intervals, rational):

   assert isinstance(rational, (int, Fraction)) and 0 < rational
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree or tree.magnitude == rational:
      return tree

   ratio = rational / tree.magnitude

   return IntervalTree([
      x.shift_to_rational(
         ((x.low - tree.low) * ratio) + tree.low).scale_by_rational(ratio) \
         for x in tree
   ])
