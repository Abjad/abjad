from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def shift_aggregate_offset_to_rational(intervals, rational):
   '''Shift the aggregate offset of `intervals` to
   `rational` ::

      abjad> a = BoundedInterval(-1, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 16)
      abjad> tree = IntervalTree([a, b, c])
      abjad> shift_aggregate_offset_to_rational(tree, Fraction(10, 7))
      IntervalTree([
         BoundedInterval(Fraction(10, 7), Fraction(38, 7), data = {}),
         BoundedInterval(Fraction(59, 7), Fraction(101, 7), data = {}),
         BoundedInterval(Fraction(80, 7), Fraction(129, 7), data = {})
      ])
   '''

   assert isinstance(rational, (int, Fraction))
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree or rational == tree.low:
      return tree

   shift = rational - tree.low

   return IntervalTree([
      x.shift_by_rational(rational - tree.low) for x in tree
   ])
