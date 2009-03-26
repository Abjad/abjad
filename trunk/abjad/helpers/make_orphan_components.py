from abjad.helpers.assert_components import assert_components
from abjad.helpers.components_detach_parentage import \
   _components_detach_parentage


def _make_orphan_components(components):
   '''Detach all components in list from parentage.
      Return list of orphan components.'''

   ## check input
   assert_components(components)

   ## detach from parentage
   _components_detach_parentage(components)

   ## return component list
   return components
