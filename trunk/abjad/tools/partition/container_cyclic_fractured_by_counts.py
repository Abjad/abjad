from abjad.container.container import Container
from abjad.tools import split


def container_cyclic_fractured_by_counts(container, counts):
   '''Partition container into parts of lengths equal to counts.
      Fracture spanners attaching directly to container.
      Leave spanners attaching to container contents untouched.
      Return Python list of partitioned parts.'''

   assert isinstance(container, Container)
   assert isinstance(counts, list)
   assert all([isinstance(x, int) and 0 < x for x in counts])

   result = [ ]

   left, right = None, container
   i = 0
   len_counts = len(counts)
   if len_counts:
      while 1 < len(right):
         count = counts[i % len_counts]
         left, right = split.fractured_at_index(right, count)
         result.append(left)
         i += 1
      if len(right):
         result.append(right)
   else:
      result.append(container)

   return result
