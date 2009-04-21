from abjad.tools.partition._by_durations import _by_durations as \
   partition__by_durations


def fractured_by_durations(components, durations):

   return partition__by_durations(
      components, durations, spanners = 'fractured')
