from abjad.helpers.assert_components import assert_components
from abjad.helpers.components_switch_parent_to import \
   _components_switch_parent_to


def _make_orphan_components(components):
   '''Detach all components in list from parentage.
      Return list of orphan components.'''

   ## check input
   assert_components(components)

   ## detach from parentage
   _components_switch_parent_to(components, None)

   ## return component list
   return components
