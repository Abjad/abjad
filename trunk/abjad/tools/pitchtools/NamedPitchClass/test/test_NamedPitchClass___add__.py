from abjad import *


def test_NamedPitchClass___add___01( ):

   npc = pitchtools.NamedPitchClass('c')

   new = npc + pitchtools.MelodicDiatonicInterval('perfect', 1)
   new == pitchtools.NamedPitchClass('c')

   new = npc + pitchtools.MelodicDiatonicInterval('minor', 2)
   new == pitchtools.NamedPitchClass('df')

   new = npc + pitchtools.MelodicDiatonicInterval('minor', -2)
   new == pitchtools.NamedPitchClass('b')

   new = npc + pitchtools.MelodicDiatonicInterval('major', 2)
   new == pitchtools.NamedPitchClass('d')

   new = npc + pitchtools.MelodicDiatonicInterval('major', -2)
   new == pitchtools.NamedPitchClass('bf')
