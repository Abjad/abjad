from abjad import *


def test_NumericPitchClassSet_multiply_01( ):

   assert pitchtools.NumericPitchClassSet([0, 1, 5]).multiply(5) == \
      pitchtools.NumericPitchClassSet([0, 1, 5])
   assert pitchtools.NumericPitchClassSet([1, 2, 6]).multiply(5) == \
      pitchtools.NumericPitchClassSet([5, 6, 10])
   assert pitchtools.NumericPitchClassSet([2, 3, 7]).multiply(5) == \
      pitchtools.NumericPitchClassSet([3, 10, 11])
