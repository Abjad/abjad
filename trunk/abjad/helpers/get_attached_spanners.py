from abjad.helpers.are_strictly_contiguous_components_in_same_thread import _are_strictly_contiguous_components_in_same_thread


def _get_attached_spanners(components):
   '''TODO: Write doc string.
      TODO: Include example.'''

   ## check input
   if not _are_strictly_contiguous_components_in_same_thread(components):
      raise ContiguityError(
         'Input must be strictly contiguous components in same thread.')
   
   ## accumulate spanners
   spanners = set([ ])
   for component in components:
      for spanner in list(component.spanners.attached):
         spanners.update((spanner, ))
      
   ## return spanners
   return spanners
