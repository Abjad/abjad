from abjad import *


def test_seqtools_yield_all_permutations_of_sequence_01( ):
   
   l = [1, 2, 3]
   t = seqtools.yield_all_permutations_of_sequence(l)
   t = list(t)

   assert t == [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
