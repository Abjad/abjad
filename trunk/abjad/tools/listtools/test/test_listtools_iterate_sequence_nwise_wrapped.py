from abjad import *


def test_listtools_iterate_sequence_nwise_wrapped_01( ):

   t = list(listtools.iterate_sequence_nwise_wrapped(range(6), 3))
   assert t == [(0, 1, 2), (1, 2, 3), (2, 3, 4), 
      (3, 4, 5), (4, 5, 0), (5, 0, 1)]
