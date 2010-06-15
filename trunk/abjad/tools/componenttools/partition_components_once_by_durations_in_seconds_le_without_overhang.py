from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_once_by_durations_in_seconds_le_without_overhang(
   components, prolated_durations):
   '''Partition `components` once by durations in seconds that equal
   or are just less than `prolated_durations` and
   do not allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations(
      'prolated', components, prolated_duration, 
      fill = 'less', cyclic = False, overhang = False)

   return parts
