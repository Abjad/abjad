from abjad.helpers.assert_components import _assert_components


## TODO: Make non-composer-safe helper private. ##

def components_detach_parentage(components):
   '''Detach parent from every Abjad component in list.
      Components need not be successive.
      Return newly orphaned components.
      Note that components_detach_parentage_deep makes no sense.'''

   _assert_components(components)

   for component in components:
      component.parentage._detach( )
   return components
