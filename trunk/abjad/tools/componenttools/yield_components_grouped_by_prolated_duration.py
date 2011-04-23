def yield_components_grouped_by_prolated_duration(components):
   '''.. versionadded:: 1.1.2

   Yield successive tuples from `components` with like
   prolated duration. ::

      abjad> notes = notetools.make_notes([0], [(1, 4), (1, 4), (1, 8), (1, 16), (1, 16), (1, 16)])
      abjad> for x in componenttools.yield_components_grouped_by_prolated_duration(notes):
      ...     x
      ... 
      (Note(c', 4), Note(c', 4))
      (Note(c', 8),)
      (Note(c', 16), Note(c', 16), Note(c', 16))
   '''
      
   cur_group = [ ]
   for component in components:
      if cur_group:
         prev_component = cur_group[-1]
         prev_duration = prev_component.duration.prolated
         cur_duration = component.duration.prolated
         if cur_duration == prev_duration:
            cur_group.append(component)
         else:
            yield tuple(cur_group)
            cur_group = [ ]
            cur_group.append(component)
      else:
         cur_group.append(component)
   if cur_group:
      yield tuple(cur_group)
