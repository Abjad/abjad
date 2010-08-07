from abjad import *


def test_PitchClassSet_is_transposed_superset_01( ):

   small = pitchtools.NumericPitchClassSet([9, 10, 11])
   big = pitchtools.NumericPitchClassSet([0, 1, 2, 3])

   assert big.is_transposed_superset(small)
   assert not small.is_transposed_superset(big)


def test_PitchClassSet_is_transposed_superset_02( ):

   small = pitchtools.NumericPitchClassSet([5, 7, 9])
   big = pitchtools.NumericPitchClassSet([0, 1, 2, 3])

   assert not big.is_transposed_superset(small)
   assert not small.is_transposed_superset(big)
