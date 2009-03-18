from abjad.helpers.assert_components import _assert_are_strictly_contiguous_components_in_same_thread


def _get_attached_spanners(components):
   '''TODO: Write doc string.
      TODO: Include example.'''

   ## check input
   _assert_are_strictly_contiguous_components_in_same_thread(components)
   
   ## accumulate spanners
   spanners = set([ ])
   for component in components:
      for spanner in list(component.spanners.attached):
         spanners.update((spanner, ))
      
   ## return spanners
   return spanners
