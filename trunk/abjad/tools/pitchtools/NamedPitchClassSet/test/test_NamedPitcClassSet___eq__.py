from abjad import *


def test_NamedPitchClassSet___eq___01( ):
   '''Named pitch class set equality works as expected.'''

   npc_set_1 = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),])

   npc_set_2 = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('c'),
      pitchtools.NamedPitchClass('d'),
      pitchtools.NamedPitchClass('e'),])

   npc_set_3 = pitchtools.NamedPitchClassSet([
      pitchtools.NamedPitchClass('e'),
      pitchtools.NamedPitchClass('f'),
      pitchtools.NamedPitchClass('g'),])

   assert npc_set_1 == npc_set_1
   assert npc_set_1 == npc_set_2
   assert npc_set_1 != npc_set_3
   assert npc_set_2 != npc_set_3
