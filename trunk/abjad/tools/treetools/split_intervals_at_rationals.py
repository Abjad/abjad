from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def split_intervals_at_rationals(intervals, rationals):
   '''Split `intervals` at each rational in 
   `rationals` ::

      abjad> a = BoundedInterval(-1, 3)
      abjad> b = BoundedInterval(6, 12)
      abjad> c = BoundedInterval(9, 16)
      abjad> tree = IntervalTree([a, b, c])
      abjad> split_intervals_at_rationals(tree, [1, Fraction(19, 2)])
      IntervalTree([
         BoundedInterval(-1, 1, data = {}),
         BoundedInterval(1, 3, data = {}),
         BoundedInterval(6, Fraction(19, 2), data = {}),
         BoundedInterval(9, Fraction(19, 2), data = {}),
         BoundedInterval(Fraction(19, 2), 12, data = {}),
         BoundedInterval(Fraction(19, 2), 16, data = {})
      ]) 
   '''

   assert len(rationals)
   assert all([isinstance(x, (int, Fraction)) for x in rationals])
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree or not rationals:
      return tree

   for rational in rationals:
      tree = IntervalTree([x.split_at_rational(rational) for x in tree])

   return tree
