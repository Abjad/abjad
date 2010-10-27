import itertools


def yield_all_permutations_of_sequence(sequence):
   '''Yield all permutations of `sequence`::

      abjad> list(seqtools.yield_all_permutations_of_sequence([1, 2, 3]))
      [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

   Return generator of tuples.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.permutations( )`` to
      ``seqtools.yield_all_permutations_of_sequence( )``.
   '''

   return itertools.permutations(sequence)
