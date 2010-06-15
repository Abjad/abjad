from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_cyclically_by_durations_in_seconds_le_with_overhang(
   components, durations_in_seconds):
   '''Partition `components` cyclically by durations in seconds equal to
   or just less than `durations_in_seconds` and
   allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations('prolated', components, prolated_duration, 
      fill = 'less', cyclic = True, overhang = True)

   return parts
