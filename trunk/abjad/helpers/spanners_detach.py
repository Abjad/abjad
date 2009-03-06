from abjad.helpers.are_components import _are_components
from abjad.helpers.iterate import iterate


def spanners_detach(components, level = 'top'):
   '''With level = 'flat':
         detach spanners from every Abjad component at top level of list.
      With level = 'all':
         detach spanners from every Abjad component at all levels of list.

      Return None.
   '''

   # check input
   if not _are_components(components):
      raise ValueError('input must be Python list of components.')

   # delegate
   if level == 'top':
      _spanners_detach_top(components)
   elif level == 'all':
      _spanners_detach_all(components)
   else:
      raise ValueError("level must be 'top' or 'all'.")


def _spanners_detach_all(components):
   '''Detach spanners from every Abjad component at all levels of list.'''
   for component in iterate(components, '_Component'):
      component.spanners.detach( )


def _spanners_detach_top(components):
   '''Detach spanners from every Abjad component at top level of list.'''
   for component in components:
      try:
         component.spanners.detach( )
      except AttributeError:
         pass
