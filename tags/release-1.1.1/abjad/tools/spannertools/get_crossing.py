from abjad.component.component import _Component
from abjad.tools import check
from abjad.tools import iterate
from abjad.tools.spannertools.get_contained import get_contained
from abjad.tools.spannertools.get_covered import get_covered


def get_crossing(components):
   '''Assert thread-contiguous components.
      Collect spanners that attach to any component in 'components'.
      Return unordered set of crossing spanners.
      A spanner P crosses a list of thread-contiguous components C
      when P and C share at least one component and when it is the
      case that NOT ALL of the components in P are also in C.
      In other words, there is some intersection -- but not total
      intersection -- between the components of P and C.

      Compare 'crossing' spanners with 'covered' spanners.
      Compare 'crossing' spanners with 'dominant' spanners.
      Compare 'crossing' spanners with 'contained' spanners.
      Compare 'crossing' spanners with 'attached' spanners.'''

   check.assert_components(components, contiguity = 'thread')

#   result = get_contained(components) - \
#      get_covered(components)

   all_components = set(iterate.naive(components, _Component))
   contained_spanners = get_contained(components)
   crossing_spanners = set([ ])
   for spanner in contained_spanners:
      spanner_components = set(spanner[:])
      if not spanner_components.issubset(all_components):
         crossing_spanners.add(spanner)
   
   return crossing_spanners
