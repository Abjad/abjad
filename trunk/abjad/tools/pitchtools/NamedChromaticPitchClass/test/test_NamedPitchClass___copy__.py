from abjad import *
import copy


def test_NamedPitchClass___copy___01( ):

   npc = pitchtools.NamedChromaticPitchClass('cs')
   new = copy.copy(npc)

   assert new == npc
   assert new is not npc
