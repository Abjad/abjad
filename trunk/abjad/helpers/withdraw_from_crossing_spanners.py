from abjad.component.component import _Component
from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_crossing_spanners import get_crossing_spanners
from abjad.helpers.iterate import iterate


def _withdraw_from_crossing_spanners(components):
   '''This operation can leave score trees in a weird state.
      Operation should only be used in the middle of some other operation.
      Intended purpose is to strip components of crosssing spanners.
      Similar to stripping components of parentage.
      These two operations prepared components for reincorporation.
      Reincorporation means setting into some other score tree.
      Container setitem is probably primary consumer of this operation.
      Return None.'''

   assert_components(components, contiguity = 'thread')

   crossing_spanners = get_crossing_spanners(components) 

   components_including_children = list(iterate(components, _Component))

   for crossing_spanner in list(crossing_spanners):
      spanner_components = crossing_spanner._components[:]
      for component in components_including_children:
         if component in spanner_components:
            crossing_spanner._components.remove(component)
            component.spanners._spanners.discard(crossing_spanner)
