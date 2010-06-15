from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_cyclically_by_prolated_durations_le_without_overhang(
   components, prolated_durations):
   '''Partition `components` cyclically by prolated durations that equal
   or are just less than `prolated_durations` and
   do not allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations(
      'prolated', components, prolated_duration, 
      fill = 'less', cyclic = True, overhang = False)

   return parts
