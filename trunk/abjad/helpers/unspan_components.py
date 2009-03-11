from abjad.helpers.are_components import _are_components


def unspan_components(components):
   '''Input parameter:

      component_list should be a Python list of any Abjad components.

      Description:
      
      Unspan every component in components.
      Does not navigate down into components; traverse shallowly.
      Return components.

      Note that you can leave noncontiguous notes spanned
      after apply unspan_components to components in the
      middle of some larger spanner.'''

   # check input
   if not _are_components(components):
      raise ValueError('input must be Python list of Abjad components.')

   # detach spanners
   for component in components:
      component.spanners.detach( )   

   # return components
   return components
