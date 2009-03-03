from abjad.helpers.are_components import _are_components


def unspan_components(component_list):
   '''Unspan every component in component_list;
      return component_list.

      Does not navigate down into component_list;
      traverses component_list shallowly.

      Note that you can leave noncontiguous notes spanned
      after apply unspan_components to components in the
      middle of some larger spanner.'''

   if not _are_components(component_list):
      raise ValueError('component_list must be Abjad components.')

   for component in component_list:
      component.spanners.detach( )   

   return component_list
