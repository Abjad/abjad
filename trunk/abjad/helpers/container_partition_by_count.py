from abjad.container.container import Container
from abjad.helpers.cumulative_sums import cumulative_sums
from abjad.helpers.lcopy import lcopy
from abjad.helpers.pairwise import pairwise


## TODO: Possibly implement this as a generalization of lcopy( )?

def container_partition_by_count(container, counts):
   r'''container is any Abjad container to partition.
      counts is a Python list of zero or more positive integers.

      Partition container and all parents of container.
      Do not act in place.
      Instead, return list of parts equal in number to len(counts).

      The helpers wraps lcopy( ).
      This means that the original structure remains unchanged.
      Also that resulting parts cut all the way up into voice.
   
      Example:

      t = Voice([FixedDurationTuplet((2, 8), scale(3))])
      Beam(t[0][:])
      left, right = container_partition_by_count(t[0], [1, 2])

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
   sums = [0] + cumulative_sums(counts)
   for start, stop in pairwise(sums):
      result.append(lcopy(container, start, stop))

   return result
