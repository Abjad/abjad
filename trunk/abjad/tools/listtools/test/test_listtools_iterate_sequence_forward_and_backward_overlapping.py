from abjad import *


def test_listtools_iterate_sequence_forward_and_backward_overlapping_01( ):

   g = listtools._generator(1, 6)
   t = list(listtools.iterate_sequence_forward_and_backward_overlapping(g))
   
   assert t == [1, 2, 3, 4, 5, 4, 3, 2]
