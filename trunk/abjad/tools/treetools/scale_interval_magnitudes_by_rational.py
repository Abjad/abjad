from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def scale_interval_magnitudes_by_rational(intervals, rational):
   '''Scale the magnitude of each interval in `intervals` by
   `rational`, maintaining their low offsets ::

      abjad> a = BoundedInterval(-1, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 16)
      abjad> tree = IntervalTree([a, b, c])
      abjad> scale_interval_magnitudes_by_rational(tree, Fraction(6, 5))
      IntervalTree([
         BoundedInterval(-1, Fraction(19, 5), data = {}),
         BoundedInterval(6, Fraction(66, 5), data = {}),
         BoundedInterval(9, Fraction(87, 5), data = {})
      ])
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
      x.scale_by_rational(rational) for x in tree
   ])
