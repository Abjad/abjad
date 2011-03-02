from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty


def calculate_sustain_centroid_of_intervals(intervals):
   '''Return a weighted mean, such that the centroid of each interval
   in `intervals` are the values, and the weights are their magnitudes.
   '''
       
   assert all_are_intervals_or_trees_or_empty(intervals)
   tree = IntervalTree(intervals)   

   return sum([(x.centroid * x.magnitude) for x in tree]) / \
      sum([x.magnitude for x in tree])
   
