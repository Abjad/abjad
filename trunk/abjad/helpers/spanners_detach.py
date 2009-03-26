from abjad.helpers.assert_components import assert_components
from abjad.helpers.iterate import iterate


## TODO: Rename as components_spanners_detach( )

def spanners_detach(components, level = 'top'):
   '''With level = 'flat':
         detach spanners from every Abjad component at top level of list.
      With level = 'all':
         detach spanners from every Abjad component at all levels of list.

      Return None.'''

   # check input
   assert_components(components)

   # delegate
   if level == 'top':
      _spanners_detach_top(components)
   elif level == 'all':
      _spanners_detach_all(components)
   else:
      raise ValueError("level must be 'top' or 'all'.")


def _spanners_detach_all(components):
   '''Detach spanners from every Abjad component at all levels of list.'''
   from abjad.component.component import _Component
   for component in iterate(components, _Component):
      component.spanners._detach( )


def _spanners_detach_top(components):
   '''Detach spanners from every Abjad component at top level of list.'''
   for component in components:
      try:
         component.spanners._detach( )
      except AttributeError:
         pass
