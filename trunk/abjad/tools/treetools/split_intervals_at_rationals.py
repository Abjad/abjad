from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def split_intervals_at_rationals(intervals, rationals):

   assert len(rationals)
   assert all([isinstance(x, (int, Fraction)) for x in rationals])
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)
   if not tree or not rationals:
      return tree

   for rational in rationals:
       tree = IntervalTree([x.split_at_rational(rational) for x in tree])

   return tree
