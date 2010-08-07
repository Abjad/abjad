from abjad import *


def test_PitchClassSet_transpose_01( ):

   pcset = pitchtools.NumericPitchClassSet([1, 2, 5])
   assert pcset.transpose(0) == pitchtools.NumericPitchClassSet([1, 2, 5])
   assert pcset.transpose(1) == pitchtools.NumericPitchClassSet([2, 3, 6])
   assert pcset.transpose(2) == pitchtools.NumericPitchClassSet([3, 4, 7])
   assert pcset.transpose(3) == pitchtools.NumericPitchClassSet([4, 5, 8])
   assert pcset.transpose(4) == pitchtools.NumericPitchClassSet([5, 6, 9])
   assert pcset.transpose(5) == pitchtools.NumericPitchClassSet([6, 7, 10])
   assert pcset.transpose(6) == pitchtools.NumericPitchClassSet([7, 8, 11])
   assert pcset.transpose(7) == pitchtools.NumericPitchClassSet([8, 9, 0])
   assert pcset.transpose(8) == pitchtools.NumericPitchClassSet([9, 10, 1])
   assert pcset.transpose(9) == pitchtools.NumericPitchClassSet([10, 11, 2])
   assert pcset.transpose(10) == pitchtools.NumericPitchClassSet([11, 0, 3])
   assert pcset.transpose(11) == pitchtools.NumericPitchClassSet([0, 1, 4])
