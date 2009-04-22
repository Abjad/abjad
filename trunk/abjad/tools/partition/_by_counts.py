from abjad.tools import check
from abjad.tools.split._at_index import _at_index as split__at_index


def _by_counts(container, counts, spanners = 'unfractured', cyclic = False):
   '''Partition Python list of components into parts of lengths in counts.
      Fracture spanners or not according to keyword.
      Return Python list of partitioned parts.'''

   check.assert_components([container])
   assert isinstance(counts, list)
   assert all([isinstance(x, (int)) and 0 < x for x in counts])

   result = [ ]

   left, right = None, container
   i = 0
   len_counts = len(counts)
   if len_counts:
      while 1 < len(right):
         try:
            if cyclic:
               count = counts[i % len_counts]
            else:
               count = counts[i]
         except IndexError:
            break
         left, right = split__at_index(right, count, spanners = spanners)
         result.append(left)
         i += 1
      if len(right):
         result.append(right)
   else:
      result.append(container)

   return result
