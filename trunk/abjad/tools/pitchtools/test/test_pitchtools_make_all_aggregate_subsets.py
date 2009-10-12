from abjad import *


def test_pitchtools_make_all_aggregate_subsets_01( ):

   U_star = pitchtools.make_all_aggregate_subsets( )
   assert len(U_star) == 4096
   assert pitchtools.PitchClassSet([0, 1, 2]) in U_star
   assert pitchtools.PitchClassSet([1, 2, 3]) in U_star
   assert pitchtools.PitchClassSet([3, 4, 8, 9, 11]) in U_star
   assert pitchtools.PitchClassSet(range(12)) in U_star
