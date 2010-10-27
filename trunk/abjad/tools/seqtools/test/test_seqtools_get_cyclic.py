from abjad import *


def test_seqtools_get_cyclic_01( ):
   
   l = range(20)
   t = seqtools.get_cyclic(l, 18, 10)

   assert list(t) == [18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_seqtools_get_cyclic_02( ):

   l = range(20)
   t = seqtools.get_cyclic(l, 10, 18)
   assert list(t) == [10, 11, 12, 13, 14, 15, 16, 17]

   t = seqtools.get_cyclic(l, 10, 10)
   assert list(t) == [ ]
