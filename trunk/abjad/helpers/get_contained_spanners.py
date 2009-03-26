from abjad.helpers.assert_components import assert_components


def _get_contained_spanners(components):
   '''Return unordered set of spanners contained within
      any component in list of thread-contiguous components.
      Getter for t.spanners.contained across thread-contiguous components.'''

   assert_components(components, contiguity = 'thread')

   result = set([ ]) 
   for component in components:
      result.update(component.spanners.contained)

   return result
