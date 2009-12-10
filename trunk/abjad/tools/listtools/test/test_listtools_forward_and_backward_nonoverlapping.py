from abjad import *


def test_listtools_forward_and_backward_nonoverlapping_01( ):

   g = listtools._generator(1, 6)
   t = list(listtools.forward_and_backward_nonoverlapping(g))
   
   assert t == [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
