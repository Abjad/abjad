from abjad import *


def test_seqtools_iterate_sequence_forward_and_backward_nonoverlapping_01( ):

   t = list(seqtools.iterate_sequence_forward_and_backward_nonoverlapping(xrange(1, 6)))
   
   assert t == [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
