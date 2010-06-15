from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_cyclically_by_prolated_durations_exactly_with_overhang(
   components, prolated_durations):
   '''Partition `components` cyclically by exact `prolated_durations` and
   allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations(
      'prolated', components, prolated_durations, 
      fill = 'exact', cyclic = True, overhang = True)

   return parts
