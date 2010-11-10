from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_once_by_prolated_durations_ge_without_overhang(components, prolated_durations):
   '''Partition `components` cyclically by prolated durations that equal
   or are just greater than `prolated_durations` and
   do not allow for overhang components at end.
   '''
   
   parts = _partition_components_by_durations('prolated', components, prolated_durations, 
      fill = 'greater', cyclic = False, overhang = False)

   return parts
