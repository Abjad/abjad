from abjad.helpers.assert_components import _assert_components
from abjad.helpers.components_detach_parentage import components_detach_parentage


def _make_orphan_components(components):
   '''Detach all components in list from parentage.
      Return list of orphan components.'''

   ## check input
   _assert_components(components)

   ## detach from parentage
   components_detach_parentage(components)

   ## return component list
   return components
