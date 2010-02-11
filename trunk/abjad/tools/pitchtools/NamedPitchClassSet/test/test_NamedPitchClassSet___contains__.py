from abjad import *


def test_PitchClassSet___contains___01( ):
   '''NamedPitchClassSet containment works as expected.'''

   npc_set = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),])

   assert pitchtools.NamedPitchClass('c') in npc_set
   assert pitchtools.NamedPitchClass('d') in npc_set
   assert pitchtools.NamedPitchClass('e') in npc_set

   assert not pitchtools.NamedPitchClass('cs') in npc_set
   assert not pitchtools.NamedPitchClass('cf') in npc_set
