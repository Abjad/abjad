from abjad.tools import mathtools
from abjad.tools.seqtools.all_are_equal import all_are_equal
from abjad.tools.seqtools.partition_sequence_cyclically_by_counts_without_overhang import \
   partition_sequence_cyclically_by_counts_without_overhang


def sequence_to_period_of_rotation(sequence, n):
   '''.. versionadded:: 1.1.2

   Change `sequence` to period of rotation:
   
      abjad> seqtools.sequence_to_period_of_rotation([1, 1, 1, 1, 1, 1])
      1

   ::

      abjad> seqtools.sequence_to_period_of_rotation([1, 1, 2, 1, 1, 1])
      6

   ::

      abjad> seqtools.sequence_to_period_of_rotation([1, 1, 2, 1, 1, 2])
      3

   None when `sequence` is empty. ::

      abjad> seqtools.sequence_to_period_of_rotation([ ]) is None
      True

   Return nonegative integer.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.get_period( )`` to
      ``seqtools.sequence_to_period_of_rotation( )``.
   '''
   
   sequence = list(sequence)
   if not sequence:
      return None
   for factor in sorted(mathtools.divisors(len(sequence))):
      #print 'factor is %s ...' % factor
      parts = partition_sequence_cyclically_by_counts_without_overhang(sequence, [factor])
      if all_are_equal(parts):
         return factor
   return factor
