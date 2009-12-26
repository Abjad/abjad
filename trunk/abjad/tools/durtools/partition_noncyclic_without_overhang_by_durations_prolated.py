from abjad.exceptions import PartitionError
from abjad.rational import Rational


def partition_noncyclic_without_overhang_by_durations_prolated(components, 
   prolated_durations):
   '''.. versionadded:: 1.1.2

   Yield tuples from `components` equal to successive `prolated_durations`. ::

      abjad> notes = construct.notes([0], [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)])
      abjad> pitchtools.diatonicize(notes)
      abjad> for part in durtools.partition_noncyclic_with_overhang_by_durations_prolated(notes, [(1, 4)]):
      ...   part
      ...
      (Note(c', 8), Note(d', 8))

   Raise partition error where `components` can not match
   `prolated_durations`. ::

      abjad> for part in durtools.partition_noncyclic_with_overhang_by_durations_prolated(notes, [(3, 16)]):
      ...   part
      ...
      PartitionError
   '''

   cur_part, cur_sum = [ ], Rational(0)
   prolated_durations = list(prolated_durations)
   cur_prolated_duration = Rational(prolated_durations.pop(0))

   for i, component in enumerate(components):
      cur_part.append(component)
      cur_sum += component.duration.prolated
      if cur_sum == cur_prolated_duration:
         yield tuple(cur_part)
         try:
            cur_prolated_duration = Rational(prolated_durations.pop(0))
         except IndexError:
            break
         cur_part, cur_sum = [ ], Rational(0)
      elif cur_prolated_duration < cur_sum:
         raise PartitionError('component durations do not fit.')
