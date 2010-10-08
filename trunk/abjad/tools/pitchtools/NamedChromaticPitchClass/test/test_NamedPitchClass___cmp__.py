from abjad import *


def test_NamedPitchClass___cmp___01( ):
   '''Referentially equal named pitch classes compare equally.'''

   npc = pitchtools.NamedChromaticPitchClass('fs')
   assert     npc == npc
   assert not npc != npc
   assert not npc >  npc
   assert     npc >= npc
   assert not npc <  npc
   assert     npc <= npc


def test_NamedPitchClass___cmp___02( ):
   '''Different letter strings.'''

   npc_1 = pitchtools.NamedChromaticPitchClass('fs')
   npc_2 = pitchtools.NamedChromaticPitchClass('gf')
   assert not npc_1 == npc_2
   assert     npc_1 != npc_2
   assert not npc_1 >  npc_2
   assert not npc_1 >= npc_2
   assert     npc_1 <  npc_2
   assert     npc_1 <= npc_2 


def test_NamedPitchClass___cmp___03( ):
   '''Same letter strings.'''

   npc_1 = pitchtools.NamedChromaticPitchClass('f')
   npc_2 = pitchtools.NamedChromaticPitchClass('fs')
   assert not npc_1 == npc_2
   assert     npc_1 != npc_2
   assert not npc_1 >  npc_2
   assert not npc_1 >= npc_2
   assert     npc_1 <  npc_2
   assert     npc_1 <= npc_2 
