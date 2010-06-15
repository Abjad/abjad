from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_once_by_durations_in_seconds_exactly_without_overhang(
   components, durations_in_seconds):
   '''Partition `components` cyclically by exact `durations_in_seconds` and
   do not allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations(
      'seconds', components, durations_in_seconds, 
      fill = 'exact', cyclic = False, overhang = False)

   return parts
