from abjad import *


def test_seqtools_iterate_sequence_forward_and_backward_overlapping_01( ):

   g = seqtools.generate_range(1, 6)
   t = list(seqtools.iterate_sequence_forward_and_backward_overlapping(g))
   
   assert t == [1, 2, 3, 4, 5, 4, 3, 2]
