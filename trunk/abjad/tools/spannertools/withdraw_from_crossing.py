from abjad.component import _Component
from abjad.tools import check
from abjad.tools import iterate
from abjad.tools.spannertools.get_crossing import get_crossing


def _withdraw_from_crossing(components):
   '''This operation can leave score trees in a weird state.
   Operation should only be used in the middle of some other operation.
   Intended purpose is to strip components of crosssing spanners.
   Similar to stripping components of parentage.
   These two operations prepared components for reincorporation.
   Reincorporation means setting into some other score tree.
   Container setitem is probably primary consumer of this operation.
   Return None.
   '''

   check.assert_components(components, contiguity = 'thread')

   crossing_spanners = get_crossing(components) 

   components_including_children = list(
      iterate.naive_forward_in(components, _Component))

   for crossing_spanner in list(crossing_spanners):
      spanner_components = crossing_spanner._components[:]
      for component in components_including_children:
         if component in spanner_components:
            crossing_spanner._components.remove(component)
            component.spanners._spanners.discard(crossing_spanner)
