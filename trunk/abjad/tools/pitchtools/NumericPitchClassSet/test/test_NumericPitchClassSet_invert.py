from abjad import *


def test_NumericPitchClassSet_invert_01( ):

   assert pitchtools.NumericPitchClassSet([0, 1, 5]).invert( ) == \
      pitchtools.NumericPitchClassSet([0, 7, 11])
   assert pitchtools.NumericPitchClassSet([1, 2, 6]).invert( ) == \
      pitchtools.NumericPitchClassSet([6, 10, 11])
