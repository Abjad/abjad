from abjad import *


def test_seqtools_overwrite_slices_at_01( ):

   l = range(10)
   t = seqtools.overwrite_slices_at(l, [(0, 3), (5, 3)])

   assert t == [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]


def test_seqtools_overwrite_slices_at_02( ):

   l = range(10)
   t = seqtools.overwrite_slices_at(l, [(0, 99)])

   assert t == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
