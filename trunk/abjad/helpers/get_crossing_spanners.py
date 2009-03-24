from abjad.helpers.assert_components import _assert_components
from abjad.helpers.get_contained_spanners import _get_contained_spanners
from abjad.helpers.get_covered_spanners import _get_covered_spanners


def _get_crossing_spanners(components):
   '''Assert thread-contiguous components.
      Collect spanners that attach to any of the components,
      or component music, in 'components' but that are *not*
      completely covered by the time interval of 'components'.
      Return results as unordered set.

      Compare 'crossing' spanners with 'covered' spanners.
      Compare 'crossing' spanners with 'dominant' spanners.
      Compare 'crossing' spanners with 'contained' spanners.
      Compare 'crossing' spanners with 'attached' spanners.'''

   _assert_components(components, contiguity = 'thread')

   result = _get_contained_spanners(components) - \
      _get_covered_spanners(components)

   return result
