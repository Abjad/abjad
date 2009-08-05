def find_component_at_score_offset(spanner, score_offset):
   '''Return the component in 'spanner' that begins at
      exactly 'score_offset'.
      Otherwise return None.'''

   for component in spanner:
      if component.offset.prolated.start == score_offset:
         return component
