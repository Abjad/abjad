from abjad.tools import check


def get_contained(components):
   '''Return unordered set of spanners contained within
      any component in list of thread-contiguous components.
      Getter for t.spanners.contained across thread-contiguous components.'''

   check.assert_components(components, contiguity = 'thread')

   result = set([ ]) 
   for component in components:
      result.update(component.spanners.contained)

   return result
