from abjad.helpers.are_successive_components import _are_successive_components


def untie_components(component_list):
   '''Untie every component in component list.
      Return component list.'''

   if not _are_successive_components(component_list):
      raise ContiguityError('components must be successive.')

   for component in component_list:
      component.tie.unspan( )

   return component_list
