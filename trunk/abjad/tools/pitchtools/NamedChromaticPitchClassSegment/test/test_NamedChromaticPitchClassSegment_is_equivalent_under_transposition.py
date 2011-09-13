from abjad import *


def test_NamedChromaticPitchClassSegment_is_equivalent_under_transposition_01():

    npc_seg_1 = pitchtools.NamedChromaticPitchClassSegment(['c', 'e', 'b'])
    npc_seg_2 = pitchtools.NamedChromaticPitchClassSegment(['f', 'a', 'e'])
    npc_seg_3 = pitchtools.NamedChromaticPitchClassSegment(['f', 'a'])

    assert npc_seg_1.is_equivalent_under_transposition(npc_seg_1)
    assert npc_seg_1.is_equivalent_under_transposition(npc_seg_2)
    assert not npc_seg_1.is_equivalent_under_transposition(npc_seg_3)

    assert npc_seg_2.is_equivalent_under_transposition(npc_seg_1)
    assert npc_seg_2.is_equivalent_under_transposition(npc_seg_2)
    assert not npc_seg_2.is_equivalent_under_transposition(npc_seg_3)

    assert not npc_seg_3.is_equivalent_under_transposition(npc_seg_1)
    assert not npc_seg_3.is_equivalent_under_transposition(npc_seg_2)
    assert npc_seg_3.is_equivalent_under_transposition(npc_seg_3)
