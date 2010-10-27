from abjad import *


def test_seqtools_pairs_from_to_01( ):

   pairs = seqtools.pairs_from_to([1, 2, 3], [4, 5])
   pairs = list(pairs)

   assert pairs[0] == (1, 4)
   assert pairs[1] == (1, 5)
   assert pairs[2] == (2, 4)
   assert pairs[3] == (2, 5)
   assert pairs[4] == (3, 4)
   assert pairs[5] == (3, 5)
