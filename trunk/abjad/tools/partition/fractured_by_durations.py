from abjad.tools.partition._by_durations import _by_durations as \
   partition__by_durations


def fractured_by_durations(components, durations, tie_after = False):

   return partition__by_durations(components, durations, 
      spanners = 'fractured', tie_after = tie_after)
