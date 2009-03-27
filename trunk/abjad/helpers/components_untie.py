from abjad.helpers.assert_components import assert_components


def components_untie(components):
   '''Untie every component in 'components'.
      Return 'components'.'''

   assert_components(components, contiguity = 'thread')

   for component in components:
      component.tie.unspan( )

   return components
