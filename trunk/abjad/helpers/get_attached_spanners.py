from abjad.helpers.assert_components import assert_components


def get_attached_spanners(components):
   '''TODO: Write doc string.
      TODO: Include example.'''

   ## check input
   assert_components(components, contiguity = 'strict', share = 'thread')
   
   ## accumulate spanners
   spanners = set([ ])
   for component in components:
      for spanner in list(component.spanners.attached):
         spanners.update((spanner, ))
      
   ## return spanners
   return spanners
