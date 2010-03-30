from abjad import *


def test_NamedPitchClass_transpose_01( ):

   npc = pitchtools.NamedPitchClass('c')

   new = npc.transpose(pitchtools.MelodicDiatonicInterval('perfect', 1))
   new == pitchtools.NamedPitchClass('c')

   new = npc.transpose(pitchtools.MelodicDiatonicInterval('minor', 2))
   new == pitchtools.NamedPitchClass('df')

   new = npc.transpose(pitchtools.MelodicDiatonicInterval('minor', -2))
   new == pitchtools.NamedPitchClass('b')

   new = npc.transpose(pitchtools.MelodicDiatonicInterval('major', 2))
   new == pitchtools.NamedPitchClass('d')

   new = npc.transpose(pitchtools.MelodicDiatonicInterval('major', -2))
   new == pitchtools.NamedPitchClass('bf')
