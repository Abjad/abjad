from abjad.tools.seqtools.permute_sequence import permute_sequence
import itertools


def yield_all_permutations_of_sequence(sequence):
   '''Yield all permutations of `sequence` in lex order::

      abjad> list(seqtools.yield_all_permutations_of_sequence((1, 2, 3))
      [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

   Return generator of `sequence` objects.

   .. versionchanged:: 1.1.2
      renamed ``listtools.permutations( )`` to
      ``seqtools.yield_all_permutations_of_sequence( )``.
   '''

   for permutation in itertools.permutations(range(len(sequence))):
      yield permute_sequence(sequence, permutation)
