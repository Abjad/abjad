from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def scale_aggregate_magnitude_to_rational(intervals, rational):
   '''Scale the aggregate magnitude of all intervals in `intervals` to
   `rational`, maintaining the original low offset ::

      abjad> a = BoundedInterval(-1, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 16)
      abjad> tree = IntervalTree([a, b, c])
      abjad> scale_aggregate_magnitude_to_rational(tree, Fraction(16, 7))
      IntervalTree([
         BoundedInterval(-1, Fraction(-55, 119), data = {}),
         BoundedInterval(Fraction(-1, 17), Fraction(89, 119), data = {}),
         BoundedInterval(Fraction(41, 119), Fraction(9, 7), data = {})
      ])
   '''

   assert isinstance(rational, (int, Fraction)) and 0 < rational
   assert all_are_intervals_or_trees_or_empty(intervals)
   if isinstance(intervals, IntervalTree):
      tree = intervals
   else:
      tree = IntervalTree(intervals)
   if not tree or tree.magnitude == rational:
      return tree

   ratio = rational / tree.magnitude

   return IntervalTree([
      x.shift_to_rational(
         ((x.low - tree.low) * ratio) + tree.low).scale_by_rational(ratio) \
         for x in tree
   ])
