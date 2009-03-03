from abjad.helpers.are_components import _are_components


def _make_orphan_components(component_list):
   '''Detach all components in list from parentage;
      return list of orphan components.'''

   # check input
   if not _are_components(component_list):
      raise ValeError('must be components in list.')

   # detach all components
   for component in component_list:
      component.parentage.detach( )

   # return component list
   return component_list
