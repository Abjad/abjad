from abjad import *


def test_NamedChromaticPitchClassSegment_rotate_01():

    npc_segment_1 = pitchtools.NamedChromaticPitchClassSegment([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),
        pitchtools.NamedChromaticPitchClass('f'),
        pitchtools.NamedChromaticPitchClass('g'),])

    npc_segment_2 = pitchtools.NamedChromaticPitchClassSegment([
        pitchtools.NamedChromaticPitchClass('g'),
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),
        pitchtools.NamedChromaticPitchClass('f'),])

    assert npc_segment_1.rotate(1) == npc_segment_2
    assert npc_segment_1.rotate(-4) == npc_segment_2
    assert npc_segment_2.rotate(-1) == npc_segment_1
    assert npc_segment_2.rotate(4) == npc_segment_1
