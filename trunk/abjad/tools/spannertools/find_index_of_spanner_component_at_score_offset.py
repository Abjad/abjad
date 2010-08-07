from abjad.exceptions import SpannerPopulationError


def find_index_of_spanner_component_at_score_offset(spanner, score_offset):
   '''Return index of component in 'spanner'
      that begins at exactly 'score_offset'.
      Otherwise raise SpannerPopulationError.

   .. versionchanged:: 1.1.2
      renamed ``spannertools.find_index_at_score_offset( )`` to
      ``spannertools.find_index_of_spanner_component_at_score_offset( )``.
   '''

   for component in spanner:
      if component.offset.prolated.start == score_offset:
         return spanner.index(component)

   raise SpannerPopulationError(
      'no component in spanner at this score offset.')
