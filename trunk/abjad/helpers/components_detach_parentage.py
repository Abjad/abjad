from abjad.helpers.are_components import _are_components


def components_detach_parentage(components):
   '''Detach parent from every Abjad component in list.
      Components need not be successive.
      Return newly orphaned components.
      Note that components_detach_parentage_deep makes no sense.'''

   if not _are_components(components):
      raise ValueError('input must be Abjad components.')

   for component in components:
      component.parentage._detach( )
   return components
