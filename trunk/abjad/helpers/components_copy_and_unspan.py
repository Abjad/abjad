from abjad.helpers.assert_components import assert_components


def components_copy_and_unspan(components):
   '''Deep copy each of the components in 'components'.
      Remove all spanners attaching to any component.

      Example:'''

   assert_components(components, contiguity = 'thread')
