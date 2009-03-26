from abjad.helpers.assert_components import assert_components
from abjad.helpers.iterate import iterate


def _components_detach_spanners_deep(components):
   '''components should be a Python list of Abjad components.

      Unspan every component in components.
      Navigate down into components and traverse deeply.
      Return components.'''

   # check input
   assert_components(components)

   # detach spanners
   from abjad.component.component import _Component
   for component in iterate(components, _Component):
      component.spanners._detach( )

   # return components
   return components
