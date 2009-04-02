from abjad.exceptions.exceptions import SpannerPopulationError


def spanner_get_index_at_score_offset(spanner, score_offset):
   '''Return index of component in 'spanner'
      that begins at exactly 'score_offset'.
      Otherwise raise SpannerPopulationError.'''

   for component in spanner:
      if component.offset.score == score_offset:
         return spanner.index(component)

   raise SpannerPopulationError(
      'no component in spanner at this score offset.')
