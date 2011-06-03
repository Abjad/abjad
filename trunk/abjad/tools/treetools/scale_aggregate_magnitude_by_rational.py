from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from fractions import Fraction


def scale_aggregate_magnitude_by_rational(intervals, rational):
   '''Scale the aggregate magnitude of all intervals in `intervals` by
   `rational`, maintaining the original low offset ::

      abjad> from abjad.tools import treetools
      abjad> from abjad.tools.treetools import BoundedInterval
      abjad> from abjad.tools.treetools import IntervalTree

   ::

      abjad> a = BoundedInterval(-1, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 16)
      abjad> tree = IntervalTree([a, b, c])
      abjad> treetools.scale_aggregate_magnitude_by_rational(tree, Fraction(1, 3))
      IntervalTree([
         BoundedInterval(-1, Fraction(1, 3), {}),
         BoundedInterval(Fraction(4, 3), Fraction(10, 3), {}),
         BoundedInterval(Fraction(7, 3), Fraction(14, 3), {})
      ])

   Return interval tree.
   '''

   assert isinstance(rational, (int, Fraction)) and 0 < rational
   assert all_are_intervals_or_trees_or_empty(intervals)
   if isinstance(intervals, IntervalTree):
      tree = intervals
   else:
      tree = IntervalTree(intervals)
   if not tree or rational == 1:
      return tree

   return IntervalTree([
      x.shift_to_rational(
         ((x.low - tree.low) * rational) + tree.low).scale_by_rational(rational)\
         for x in tree
   ])
