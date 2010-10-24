import itertools


def yield_all_permutations_of_iterable(iterable):
   '''Yield all permutations of `iterable`::

      abjad> listtools.yield_all_permutations_of_iterable([1, 2, 3])
      <itertools.permutations object at 0x75dab0>

   ::

      abjad> list(_)
      [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

   Return generator.

   .. versionchanged:: 1.1.2
      renamed ``listtools.permutations( )`` to
      ``listtools.yield_all_permutations_of_iterable( )``.
   '''

   return itertools.permutations(iterable)
