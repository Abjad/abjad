from abjad.tools.componenttools._group_components_by_durations \
   import _group_components_by_durations


def partition_components_cyclically_by_durations_in_seconds_ge_with_overhang(
   components, durations_in_seconds):
   '''Partition `components` cyclically by durations greater than or
   equal to `durations_in_seconds` and allow for overhang components at end.
   '''
   
   parts = _group_components_by_durations('seconds', components, durations_in_seconds, 
      fill = 'greater', cyclic = True, overhang = True)

   return parts
