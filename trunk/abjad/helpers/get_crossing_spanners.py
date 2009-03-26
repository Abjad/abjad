from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_contained_spanners import get_contained_spanners
from abjad.helpers.get_covered_spanners import get_covered_spanners


def get_crossing_spanners(components):
   '''Assert thread-contiguous components.
      Collect spanners that attach to any of the components,
      or component music, in 'components' but that are *not*
      completely covered by the time interval of 'components'.
      Return results as unordered set.

      Compare 'crossing' spanners with 'covered' spanners.
      Compare 'crossing' spanners with 'dominant' spanners.
      Compare 'crossing' spanners with 'contained' spanners.
      Compare 'crossing' spanners with 'attached' spanners.'''

   assert_components(components, contiguity = 'thread')

   result = get_contained_spanners(components) - \
      get_covered_spanners(components)

   return result
