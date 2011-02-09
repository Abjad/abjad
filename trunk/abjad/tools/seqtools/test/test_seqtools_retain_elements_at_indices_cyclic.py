from abjad import *


def test_seqtools_retain_elements_at_indices_cyclic_01( ):

   t = seqtools.retain_elements_at_indices_cyclic(range(20), [0, 1], 5)
   assert t == [0, 1, 5, 6, 10, 11, 15, 16]

   
def test_seqtools_retain_elements_at_indices_cyclic_02( ):

   t = seqtools.retain_elements_at_indices_cyclic(range(20), [0, 1], 5, 1)
   assert t == [1, 2, 6, 7, 11, 12, 16, 17]
