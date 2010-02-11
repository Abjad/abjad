from abjad import *


def test_NamedPitchClassSet_transpose_01( ):

   npc_set_1 = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),])   

   npc_set_2 = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('df'),
      pitchtools.NamedPitchClass('ef'),
      pitchtools.NamedPitchClass('f'),])   
   
   minor_second_ascending = pitchtools.MelodicDiatonicInterval('minor', 2)
   assert npc_set_1.transpose(minor_second_ascending) == npc_set_2

   major_seventh_descending = pitchtools.MelodicDiatonicInterval('major', -7)
   assert npc_set_1.transpose(major_seventh_descending) == npc_set_2

   minor_second_descending = pitchtools.MelodicDiatonicInterval('minor', -2)
   assert npc_set_2.transpose(minor_second_descending) == npc_set_1

   major_seventh_ascending = pitchtools.MelodicDiatonicInterval('major', 7)
   assert npc_set_2.transpose(major_seventh_ascending) == npc_set_1
