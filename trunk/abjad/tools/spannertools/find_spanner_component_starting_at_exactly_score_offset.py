def find_spanner_component_starting_at_exactly_score_offset(spanner, score_offset):
   '''Return the component in 'spanner' that begins at
      exactly 'score_offset'.
      Otherwise return None.

   .. versionchanged:: 1.1.2
      renamed ``spannertools.find_component_at_score_offset( )`` to
      ``spannertools.find_spanner_component_starting_at_exactly_score_offset( )``.
   '''

   for component in spanner:
      if component.offset.prolated.start == score_offset:
         return component
