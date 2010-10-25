import itertools


def yield_all_permutations_of_sequence(iterable):
   '''Yield all permutations of `iterable`::

      abjad> listtools.yield_all_permutations_of_sequence([1, 2, 3])
      <itertools.permutations object at 0x75dab0>

   ::

      abjad> list(_)
      [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

   Return generator.

   .. versionchanged:: 1.1.2
      renamed ``listtools.permutations( )`` to
      ``listtools.yield_all_permutations_of_sequence( )``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.yield_all_permutations_of_iterable( )`` to
      ``listtools.yield_all_permutations_of_sequence( )``.
   '''

   return itertools.permutations(iterable)
