from abjad.helpers.are_components import _are_components
from abjad.helpers.iterate import iterate


def components_detach_spanners_deep(components):
   '''components should be a Python list of Abjad components.

      Unspan every component in components.
      Navigate down into components and traverse deeply.
      Return components.'''

   # check input
   if not _are_components(components):
      raise ValueError('input must be a Python list of Abjad components.')

   # detach spanners
   from abjad.component.component import _Component
   for component in iterate(components, _Component):
      component.spanners._detach( )

   # return components
   return components
