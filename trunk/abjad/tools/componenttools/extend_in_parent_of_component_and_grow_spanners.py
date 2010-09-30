def extend_in_parent_of_component_and_grow_spanners(component, new_components):
   '''.. versionadded:: 1.1.2

   Extend `new_components` in parent of `component`.

   Grow spanners.
   '''
   from abjad.tools import componenttools
   from abjad.tools import componenttools
   from abjad.tools import spannertools
   assert componenttools.all_are_components(new_components)
   insert_offset = component._offset.stop
   receipt = spannertools.get_spanners_that_dominate_components([component])
   for spanner, index in receipt:
      insert_component = spannertools.find_spanner_component_starting_at_exactly_score_offset(
         spanner, insert_offset)
      if insert_component is not None:
         insert_index = spanner.index(insert_component)
      else:
         insert_index = len(spanner)
      for new_component in reversed(new_components):
         spanner._insert(insert_index, new_component)
         new_component._spanners.add(spanner)
   parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])
   if parent is not None:
      for new_component in reversed(new_components):
         new_component.parentage._switch(parent)
         parent._music.insert(start + 1, new_component)
   return [component] + new_components
