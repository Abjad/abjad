from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from fractions import Fraction


def shift_aggregate_offset_by_rational(intervals, rational):
   '''Shift the aggregate offset of `intervals` by
   `rational` ::

      abjad> a = BoundedInterval(-1, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 16)
      abjad> tree = IntervalTree([a, b, c])
      abjad> shift_aggregate_offset_by_rational(tree, Fraction(1, 3))
      IntervalTree([
         BoundedInterval(Fraction(-2, 3), Fraction(10, 3), data = {}),
         BoundedInterval(Fraction(19, 3), Fraction(37, 3), data = {}),
         BoundedInterval(Fraction(28, 3), Fraction(49, 3), data = {})
      ])
   '''

   assert isinstance(rational, (int, Fraction))
   assert all_are_intervals_or_trees_or_empty(intervals)
   if isinstance(intervals, IntervalTree):
      tree = intervals
   else:
      tree = IntervalTree(intervals)
   if not tree or rational == 0:
      return tree

   return IntervalTree([
      x.shift_by_rational(rational) for x in tree
   ])
