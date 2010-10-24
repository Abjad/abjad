import itertools


def permutations(iterable):
   '''Yield all permutations of `iterable`::

      abjad> listtools.permutations([1, 2, 3])
      <itertools.permutations object at 0x75dab0>

   ::

      abjad> list(_)
      [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

   Return generator.
   '''

   return itertools.permutations(iterable)
