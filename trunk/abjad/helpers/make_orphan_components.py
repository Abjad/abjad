from abjad.helpers.assert_components import _assert_components


def _make_orphan_components(components):
   '''Detach all components in list from parentage.
      Return list of orphan components.'''

   # check input
   _assert_components(components)

   ## TODO: Implement components_parentage_detach_shallow( )
   for component in components:
      component.parentage._detach( )

   # return component list
   return components
