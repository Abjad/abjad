from abjad.helpers.are_components import _are_components
from abjad.helpers.iterate import iterate


def components_parentage_detach(components, level = 'top'):
   '''Detach parent from every Abjad component at
      specified level in list.

      Components need not be successive.

      Compare with spanners_detach(component, level = 'top').

      Return newly orphaned components.'''

   assert _are_components(components) 

   if level == 'all':
      return _components_parentage_detach_all(components)
   elif level == 'top':
      return _components_parentage_detach_top(components)
   else:
      raise ValueError("level must be 'top' or 'all'.")


def _components_parentage_detach_all(components):
   from abjad.component.component import _Component
   for component in list(iterate(components, _Component)):
      component.parentage._detach( )
   return components


def _components_parentage_detach_top(components):
   for component in components:
      component.parentage._detach( )
   return components
