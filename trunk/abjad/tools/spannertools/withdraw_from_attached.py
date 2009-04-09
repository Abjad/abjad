from abjad.helpers.assert_components import assert_components


def _withdraw_from_attached(components):
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
   assert_components(components)

   # detach spanners
   for component in components:
      component.spanners._detach( )   

   # return components
   return components
