from abjad.tools.partition._by_durations import _by_durations


def cyclic_fractured_by_durations(components, durations, tie_after = False):

   return _by_durations(components, durations, 
      spanners = 'fractured', cyclic = True, tie_after = tie_after)
