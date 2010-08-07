from abjad import *


def test_PitchClassSet_transpose_01( ):

   pcset = pitchtools.PitchClassSet([1, 2, 5])
   assert pcset.transpose(0) == pitchtools.PitchClassSet([1, 2, 5])
   assert pcset.transpose(1) == pitchtools.PitchClassSet([2, 3, 6])
   assert pcset.transpose(2) == pitchtools.PitchClassSet([3, 4, 7])
   assert pcset.transpose(3) == pitchtools.PitchClassSet([4, 5, 8])
   assert pcset.transpose(4) == pitchtools.PitchClassSet([5, 6, 9])
   assert pcset.transpose(5) == pitchtools.PitchClassSet([6, 7, 10])
   assert pcset.transpose(6) == pitchtools.PitchClassSet([7, 8, 11])
   assert pcset.transpose(7) == pitchtools.PitchClassSet([8, 9, 0])
   assert pcset.transpose(8) == pitchtools.PitchClassSet([9, 10, 1])
   assert pcset.transpose(9) == pitchtools.PitchClassSet([10, 11, 2])
   assert pcset.transpose(10) == pitchtools.PitchClassSet([11, 0, 3])
   assert pcset.transpose(11) == pitchtools.PitchClassSet([0, 1, 4])
