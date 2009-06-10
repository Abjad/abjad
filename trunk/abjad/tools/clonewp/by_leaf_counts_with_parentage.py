from abjad.container.container import Container
from abjad.tools import listtools
from abjad.tools import mathtools
from abjad.tools.clonewp.by_leaf_range_with_parentage import \
   by_leaf_range_with_parentage


## TODO: Implement in-place containertools.partition_by_counts( ) that doesn't climb to governor ##

def by_leaf_counts_with_parentage(container, leaf_counts):
   r'''container is any Abjad container to partition.
      leaf_counts is a Python list of zero or more positive integers.

      Partition container and all components in parentage of container.
      Do not act in place.
      Instead, return list of parts equal in number to len(leaf_counts).

      The function wraps lcopy( ).
      This means that the original structure remains unchanged.
      Also that resulting parts cut all the way up into voice.
   
      Example::

         t = Voice([FixedDurationTuplet((2, 8), construct.scale(3))])
         Beam(t[0][:])
         left, right = containertools.partition_by_leaf_counts_with_parentage(t[0], [1, 2])

         left:

         \new Voice {
                 \times 2/3 {
                         c'8 [ ]
                 }
         } 

         right:

         \new Voice {
                 \times 2/3 {
                         d'8 [
                         e'8 ]
                 }
         }'''
   
   assert isinstance(container, Container)
   assert all([isinstance(x, int) for x in leaf_counts])

   result = [ ]
   sums = mathtools.cumulative_sums_zero(leaf_counts)
   for start, stop in listtools.pairwise(sums):
      result.append(
         by_leaf_range_with_parentage(container, start, stop))

   return result
