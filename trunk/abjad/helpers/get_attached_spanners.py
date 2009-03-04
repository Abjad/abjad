from abjad.helpers.are_successive_components import _are_successive_components


def _get_attached_spanners(component_list):

   if not _are_successive_components(component_list):
      raise ContiguityError('components must be successive.')

   spanners = set([ ])
   for component in component_list:
      for spanner in list(component.spanners.attached):
         spanners.update((spanner, ))
      
   return spanners
