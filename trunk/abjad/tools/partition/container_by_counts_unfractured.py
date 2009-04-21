from abjad.container.container import Container
from abjad.tools import split


def container_by_counts_unfractured(container, counts):
   '''Partition container into parts of lengths equal to counts.
      Leave all spanners untouched.
      Return Python list of partitioned parts.'''

   assert isinstance(container, Container)
   assert isinstance(counts, list)
   assert all([isinstance(x, int) and 0 < x for x in counts])

   result = [ ]

   left, right = None, container
   for count in counts:
      left, right = split.unfractured_at_count(right, count)
      result.append(left)
      if not len(right):
         break
   if len(right):
      result.append(right)

   return result
