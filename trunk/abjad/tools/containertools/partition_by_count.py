from abjad.container.container import Container
from abjad.tools import clonewp
from abjad.tools import listtools
from abjad.tools import mathtools


## TODO: Possibly implement this as a generalization of lcopy( )? ##

## TODO: Implement an in-place version that doesn't climb to score root ##

def partition_by_count(container, counts):
   r'''container is any Abjad container to partition.
      counts is a Python list of zero or more positive integers.

      Partition container and all parents of container.
      Do not act in place.
      Instead, return list of parts equal in number to len(counts).

      The helpers wraps lcopy( ).
      This means that the original structure remains unchanged.
      Also that resulting parts cut all the way up into voice.
   
      Example:

      t = Voice([FixedDurationTuplet((2, 8), construct.scale(3))])
      Beam(t[0][:])
      left, right = containertools.partition_by_count(t[0], [1, 2])

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
   assert all([isinstance(x, int) for x in counts])

   result = [ ]
   sums = [0] + mathtools.sums(counts)
   for start, stop in listtools.pairwise(sums):
      result.append(clonewp.by_count_with_parentage(container, start, stop))

   return result
