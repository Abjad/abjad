def get_contained(components):
   '''Return unordered set of spanners contained within
      any component in list of thread-contiguous components.
      Getter for t.spanners.contained across thread-contiguous components.
   '''
   from abjad.tools import componenttools

   assert componenttools.all_are_thread_contiguous_components(components)

   result = set([ ]) 
   for component in components:
      result.update(component.spanners.contained)

   return result
