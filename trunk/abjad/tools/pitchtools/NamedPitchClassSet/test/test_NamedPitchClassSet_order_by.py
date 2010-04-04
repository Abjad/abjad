from abjad import *


def test_NamedPitchClassSet_order_by_01( ):

   npc_set = pitchtools.NamedPitchClassSet(['c', 'e', 'b'])
   npc_seg = pitchtools.NamedPitchClassSegment(['e', 'a', 'f'])
   ordered_set = npc_set.order_by(npc_seg)

   assert ordered_set == pitchtools.NamedPitchClassSegment(['b', 'e', 'c'])
