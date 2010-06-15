from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_cyclically_by_durations_in_seconds_le_without_overhang(
   components, durations_in_seconds):
   '''Partition `components` cyclically by durations in seconds that
   equal or are just less than `durations_in_seconds` and
   do not allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations('prolated', components, prolated_duration, 
      fill = 'less', cyclic = True, overhang = False)

   return parts
