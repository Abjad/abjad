from abjad.container.container import Container
from abjad.leaf.leaf import _Leaf
from abjad.tools import check
from abjad.tools.split._at_index import _at_index as split__at_index


#def _by_counts(container, counts, spanners = 'unfractured', cyclic = False):
def _by_counts(components, counts, spanners = 'unfractured', cyclic = False):
   '''Partition Python list of components into parts of lengths in counts.
      Fracture spanners or not according to keyword.
      Return Python list of partitioned parts.'''

   check.assert_components(components)
   assert isinstance(counts, list)
   assert all([isinstance(x, (int)) and 0 < x for x in counts])

   if counts == [ ]:
      return [components[:]]

   result = [ ]
   part = [ ]

   i = 0
   len_counts = len(counts)
   part = [ ]
   cum_comp_in_this_part = 0
   xx = components[:]

   while True:
      print 'loop start, result %s' % result
      if cum_comp_in_this_part == 0:
         try:
            if cyclic:
               count = counts[i % len_counts]
            else:
               count = counts[i]
         except IndexError:
            break
      try:
         x = xx.pop(0)
      except IndexError:
         break
      if isinstance(x, _Leaf):
         part.append(x)
         cum_comp_in_this_part += 1
         comp_still_needed = count - cum_comp_in_this_part
         if comp_still_needed == 0:
            split__at_index(x, 100, spanners = spanners)
      else:
         comp_still_needed = count - cum_comp_in_this_part
         left, right = split__at_index(
            x, comp_still_needed, spanners = spanners)
         part.append(left)
         cum_comp_in_this_part += len(left)
         if len(right):
            xx.insert(0, right)
         comp_still_needed = count - cum_comp_in_this_part
      if comp_still_needed == 0:
         result.append(part)
         i += 1
         cum_comp_in_this_part = 0
         part = [ ]
      elif comp_still_needed < 0:
         raise ValueError('something wrong.')

   if len(part):
      result.append(part)
   if len(xx):
      result.append(xx)

   return result
