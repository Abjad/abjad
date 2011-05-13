from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty
from abjad.tools.treetools.compute_depth_of_intervals \
   import compute_depth_of_intervals


def calculate_depth_density_of_intervals(intervals):
   '''Return a Fraction, of the magnitude of each interval in the
   depth tree of `intervals`, multiplied by the depth at that interval,
   divided by the overall magnitude of `intervals`.

   The depth density of a single interval is 1 ::

      abjad> a = BoundedInterval(0, 1)
      abjad> b = BoundedInterval(0, 1)
      abjad> c = BoundedInterval(Fraction(1, 2), 1)
      abjad> calculate_depth_density_of_intervals(a)
      Fraction(1, 1)
      abjad> calculate_depth_density_of_intervals([a, b])
      Fraction(2, 1)
      abjad> calculate_depth_density_of_intervals([a, c])
      Fraction(3, 2)
      abjad> calculate_depth_density_of_intervals([a, b, c])
      Fraction(5, 2)
   '''

   assert all_are_intervals_or_trees_or_empty(intervals)
   if isinstance(intervals, IntervalTree):
      tree = intervals
   else:
      tree = IntervalTree(intervals)

   if not tree:
      return Fraction(0)
   return Fraction(sum([x.magnitude for x in tree])) / tree.magnitude

#   depth = compute_depth_of_intervals(tree)
#   return Fraction(sum([x.magnitude * x.data['depth'] for x in depth])) \
#      / depth.magnitude
