from abjad.tools import mathtools
from abjad.tools.seqtools.sequence_to_degree_of_rotational_symmetry import \
   sequence_to_degree_of_rotational_symmetry


def sequence_to_period_of_rotation(sequence, n):
   '''.. versionadded:: 1.1.2

   Change `sequence` to period of rotation::
   
      abjad> seqtools.sequence_to_period_of_rotation([1, 2, 3, 1, 2, 3], 1)
      3

   ::

      abjad> seqtools.sequence_to_period_of_rotation([1, 2, 3, 1, 2, 3], 2)
      3

   ::

      abjad> seqtools.sequence_to_period_of_rotation([1, 2, 3, 1, 2, 3], 3)
      1

   Return positive integer.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.get_period( )`` to
      ``seqtools.sequence_to_period_of_rotation( )``.
   '''
   
   degree = sequence_to_degree_of_rotational_symmetry(sequence)
   period = len(sequence) / degree
   divisors_of_n = set(mathtools.divisors(n))
   divisors_of_period = set(mathtools.divisors(period))
   max_shared_divisor = max(divisors_of_n & divisors_of_period)
   return period / max_shared_divisor
