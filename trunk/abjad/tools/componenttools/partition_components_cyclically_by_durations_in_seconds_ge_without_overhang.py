from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_cyclically_by_durations_in_seconds_ge_without_overhang(components, durations_in_seconds):
   '''Partition `components` cyclically by durations in seconds that are
   equal to or just greater than `durations_in_seconds` 
   and do not allow for overhang components at end.
   '''
   
   parts = _partition_components_by_durations('prolated', components, prolated_duration, 
      fill = 'greater', cyclic = True, overhang = False)

   return parts
