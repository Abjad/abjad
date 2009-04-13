from abjad.tools import check


def untie_shallow(components):
   '''Untie every component in 'components'.
      Return 'components'.'''

   check.assert_components(components, contiguity = 'thread')

   for component in components:
      component.tie.unspan( )

   return components
