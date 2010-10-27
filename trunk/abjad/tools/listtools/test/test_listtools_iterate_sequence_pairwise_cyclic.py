from abjad import *


def test_listtools_iterate_sequence_pairwise_cyclic_01( ):
   '''Cyclic pairwise.'''

   t = range(6)
   pairs = listtools.iterate_sequence_pairwise_cyclic(t)
   for x in range(100):
      assert pairs.next( )
