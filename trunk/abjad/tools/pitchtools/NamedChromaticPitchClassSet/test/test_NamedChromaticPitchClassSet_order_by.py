from abjad import *


def test_NamedChromaticPitchClassSet_order_by_01():

    npc_set = pitchtools.NamedChromaticPitchClassSet(['c', 'e', 'b'])
    npc_seg = pitchtools.NamedChromaticPitchClassSegment(['e', 'a', 'f'])
    ordered_set = npc_set.order_by(npc_seg)

    assert ordered_set == pitchtools.NamedChromaticPitchClassSegment(['b', 'e', 'c'])
