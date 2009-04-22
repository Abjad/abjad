from abjad.tools import check
#from abjad.tools import split
from abjad.tools.split._at_index import _at_index as split__at_index


def _by_counts(container, counts, spanners = 'unfractured'):
   '''Partition Python list of components into parts of lengths in counts.
      Fracture spanners or not according to keyword.
      Return Python list of partitioned parts.'''

   check.assert_components([container])
   assert isinstance(counts, list)
   assert all([isinstance(x, (int)) and 0 < x for x in counts])

   result = [ ]

   left, right = None, container
   for count in counts:
      left, right = split__at_index(right, count, spanners = spanners)
      result.append(left)
      if not len(right):
         break
   if len(right):
      result.append(right)

   return result
