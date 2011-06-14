from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_intervals_are_nonoverlapping import all_intervals_are_nonoverlapping
from abjad.tools.treetools.compute_logical_xor_of_intervals import compute_logical_xor_of_intervals
from abjad.tools.treetools.mask_intervals_with_intervals import mask_intervals_with_intervals
from collections import Iterable
from fractions import Fraction


def resolve_overlaps_between_nonoverlapping_trees_excluding_remainders_less_than_rational(trees, rational):
   '''Create a nonoverlapping IntervalTree from `trees`.
   Intervals in higher-indexed trees in `trees` only appear in part or whole where they do not
   overlap intervals from lower-indexed trees, and then only where their magnitudes are equal to or greater than
   `rational` ::

      abjad> from abjad.tools import treetools
      abjad> from abjad.tools.treetools import BoundedInterval
      abjad> from abjad.tools.treetools import IntervalTree

   ::
   
      abjad> a = IntervalTree(BoundedInterval(0, 1, {'a': 1}))
      abjad> b = IntervalTree(BoundedInterval(Fraction(1, 32), Fraction(33, 32), {'b': 2})) 
      abjad> c = IntervalTree(BoundedInterval(Fraction(1, 16), Fraction(17, 16), {'c': 3})) 
      abjad> treetools.resolve_overlaps_between_nonoverlapping_trees_excluding_remainders_less_than_rational([a, b, c], Fraction(1, 16))
      IntervalTree([
         BoundedInterval(0, 1, {'a': 1}),
         BoundedInterval(1, Fraction(17, 16), {'c': 3})
      ])
   
   Return interval tree.
   '''

   assert isinstance(trees, Iterable) and len(trees) \
      and all([isinstance(x, IntervalTree) for x in trees]) \
      and all([all_intervals_are_nonoverlapping(x) for x in trees])
   assert isinstance(rational, (int, Fraction)) and 0 <= rational

   rtree = trees[0]
   for tree in trees[1:]:
      xor = compute_logical_xor_of_intervals([tree, rtree])
      masked = mask_intervals_with_intervals(tree, xor)
      rtree._insert(filter(lambda x: rational <= x.magnitude, masked))

   assert all_intervals_are_nonoverlapping(rtree)

   return rtree
