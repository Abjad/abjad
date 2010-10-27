from abjad import *


def test_seqtools_iterate_sequence_forward_and_backward_nonoverlapping_01( ):

   g = seqtools._generator(1, 6)
   t = list(seqtools.iterate_sequence_forward_and_backward_nonoverlapping(g))
   
   assert t == [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
