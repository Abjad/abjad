from abjad.helpers.assert_components import _assert_components
from abjad.helpers.get_contained_spanners import _get_contained_spanners


def _get_covered_spanners(components):
   '''Return unordered set of  spanners completely contained
      within the time bounds of thread-contiguous components.

      Compare 'covered' spanners with 'contained' spanners.
      Compare 'covered' spanners with 'dominant' spanners.'''

   _assert_components(components, contiguity = 'thread') 

   if not len(components):
      return set([ ])

   first, last = components[0], components[-1]
   components_begin = first.offset.score
   components_end = last.offset.score + last.duration.prolated

   result = _get_contained_spanners(components)
   for spanner in list(result):
      if spanner.begin < components_begin or \
         components_end < spanner.end:
         result.discard(spanner)
   
   return result  
