from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_once_by_prolated_durations_ge_with_overhang(
   components, prolated_durations):
   '''Partition `components` cyclically by prolated durations that
   equal or are just greater than `prolated_durations` and
   allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations(
      'prolated', components, prolated_durations, 
      fill = 'greater', cyclic = False, overhang = True)

   return parts
