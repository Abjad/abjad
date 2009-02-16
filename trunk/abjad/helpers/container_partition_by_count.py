from abjad.container.container import Container
from abjad.helpers.cumulative_sums import cumulative_sums
from abjad.helpers.lcopy import lcopy
from abjad.helpers.pairwise import pairwise


## TODO: Possibly implement this as a generalization of lcopy( )?

def container_partition_by_count(container, counts):
   '''Return list of new copies of container;
      Lenght of the elements in return list equal,
      in order, the integer elements in 'counts'.'''

   assert isinstance(container, Container)
   assert all([isinstance(x, int) for x in counts])

   result = [ ]
   sums = [0] + cumulative_sums(counts)
   for start, stop in pairwise(sums):
      result.append(lcopy(container, start, stop))

   return result
