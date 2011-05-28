from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def scale_interval_offsets_by_rational(intervals, rational):
   '''Scale the offset of each interval in `intervals` by
   `rational`, maintaining the lowest offset in `intervals` ::

      abjad> a = BoundedInterval(-1, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 16)
      abjad> tree = IntervalTree([a, b, c])
      abjad> scale_interval_offsets_by_rational(tree, Fraction(4, 5))
      IntervalTree([
         BoundedInterval(-1, 3, data = {}),
         BoundedInterval(Fraction(23, 5), Fraction(53, 5), data = {}),
         BoundedInterval(Fraction(7, 1), Fraction(14, 1), data = {})
      ])
   '''

   assert isinstance(rational, (int, Fraction))
   assert all_are_intervals_or_trees_or_empty(intervals)
   if isinstance(intervals, IntervalTree):
      tree = intervals
   else:
      tree = IntervalTree(intervals)
   if not tree or rational == 1:
      return tree

   return IntervalTree([
      x.shift_to_rational(((x.low - tree.low) * rational) + tree.low) \
         for x in tree
   ])   

