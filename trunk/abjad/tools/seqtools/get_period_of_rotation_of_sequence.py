from abjad.tools import mathtools
from abjad.tools.seqtools.get_degree_of_rotational_symmetry_of_sequence import \
   get_degree_of_rotational_symmetry_of_sequence


def get_period_of_rotation_of_sequence(sequence, n):
   '''.. versionadded:: 1.1.2

   Change `sequence` to period of rotation::
   
      abjad> seqtools.get_period_of_rotation_of_sequence([1, 2, 3, 1, 2, 3], 1)
      3

   ::

      abjad> seqtools.get_period_of_rotation_of_sequence([1, 2, 3, 1, 2, 3], 2)
      3

   ::

      abjad> seqtools.get_period_of_rotation_of_sequence([1, 2, 3, 1, 2, 3], 3)
      1

   Return positive integer.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.get_period( )`` to
      ``seqtools.get_period_of_rotation_of_sequence( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.sequence_to_period_of_rotation( )`` to
      ``seqtools.get_period_of_rotation_of_sequence( )``.
   '''
   
   degree = get_degree_of_rotational_symmetry_of_sequence(sequence)
   period = len(sequence) / degree
   divisors_of_n = set(mathtools.divisors(n))
   divisors_of_period = set(mathtools.divisors(period))
   max_shared_divisor = max(divisors_of_n & divisors_of_period)
   return period / max_shared_divisor
