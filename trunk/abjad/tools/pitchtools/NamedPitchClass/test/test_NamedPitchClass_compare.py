from abjad import *


def test_NamedPitchClass_compare_01( ):
   '''Referentially equal named pitch classes compare equally.'''

   npc = pitchtools.NamedPitchClass('fs')
   assert     npc == npc
   assert not npc != npc
   assert not npc >  npc
   assert     npc >= npc
   assert not npc <  npc
   assert     npc <= npc


def test_NamedPitchClass_compare_02( ):
   '''Different letter strings.'''

   npc_1 = pitchtools.NamedPitchClass('fs')
   npc_2 = pitchtools.NamedPitchClass('gf')
   assert not npc_1 == npc_2
   assert     npc_1 != npc_2
   assert not npc_1 >  npc_2
   assert not npc_1 >= npc_2
   assert     npc_1 <  npc_2
   assert     npc_1 <= npc_2 


def test_NamedPitchClass_compare_03( ):
   '''Same letter strings.'''

   npc_1 = pitchtools.NamedPitchClass('f')
   npc_2 = pitchtools.NamedPitchClass('fs')
   assert not npc_1 == npc_2
   assert     npc_1 != npc_2
   assert not npc_1 >  npc_2
   assert not npc_1 >= npc_2
   assert     npc_1 <  npc_2
   assert     npc_1 <= npc_2 
