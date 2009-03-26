from abjad.helpers.assert_components import assert_components


def _components_detach_parentage(components):
   '''Detach parent from every Abjad component in list.
      Components need not be successive.
      Return newly orphaned components.
      Note that components_detach_parentage_deep makes no sense.
      Not composer-safe.
      Preceed with a function that withdraws from spanners.'''

   assert_components(components)

   for component in components:
      component.parentage._detach( )
   return components
