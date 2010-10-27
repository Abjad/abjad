from abjad.tools import mathtools
from abjad.tools.listtools.all_are_equal import all_are_equal
from abjad.tools.listtools.partition_sequence_cyclically_by_counts_without_overhang import \
   partition_sequence_cyclically_by_counts_without_overhang


def sequence_to_degree_of_rotational_symmetry(iterable):
   '''.. versionadded:: 1.1.2

   Return positive integer period of `iterable`. ::
   
      abjad> listtools.sequence_to_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1])
      1

   ::

      abjad> listtools.sequence_to_degree_of_rotational_symmetry([1, 1, 2, 1, 1, 1])
      6

   ::

      abjad> listtools.sequence_to_degree_of_rotational_symmetry([1, 1, 2, 1, 1, 2])
      3

   None when `iterable` is empty. ::

      abjad> listtools.sequence_to_degree_of_rotational_symmetry([ ]) is None
      True

   .. versionchanged:: 1.1.2
      renamed ``listtools.get_period( )`` to
      ``listtools.sequence_to_degree_of_rotational_symmetry( )``.
   '''
   
   iterable = list(iterable)
   if not iterable:
      return None
   for factor in sorted(mathtools.divisors(len(iterable))):
      #print 'factor is %s ...' % factor
      parts = partition_sequence_cyclically_by_counts_without_overhang(iterable, [factor])
      if all_are_equal(parts):
         return factor
   return factor
