from abjad import *


def test_pitchtools_PCSet_transpose_01( ):

   pcset = pitchtools.PCSet([1, 2, 5])
   assert pcset.transpose(0) == pitchtools.PCSet([1, 2, 5])
   assert pcset.transpose(1) == pitchtools.PCSet([2, 3, 6])
   assert pcset.transpose(2) == pitchtools.PCSet([3, 4, 7])
   assert pcset.transpose(3) == pitchtools.PCSet([4, 5, 8])
   assert pcset.transpose(4) == pitchtools.PCSet([5, 6, 9])
   assert pcset.transpose(5) == pitchtools.PCSet([6, 7, 10])
   assert pcset.transpose(6) == pitchtools.PCSet([7, 8, 11])
   assert pcset.transpose(7) == pitchtools.PCSet([8, 9, 0])
   assert pcset.transpose(8) == pitchtools.PCSet([9, 10, 1])
   assert pcset.transpose(9) == pitchtools.PCSet([10, 11, 2])
   assert pcset.transpose(10) == pitchtools.PCSet([11, 0, 3])
   assert pcset.transpose(11) == pitchtools.PCSet([0, 1, 4])
