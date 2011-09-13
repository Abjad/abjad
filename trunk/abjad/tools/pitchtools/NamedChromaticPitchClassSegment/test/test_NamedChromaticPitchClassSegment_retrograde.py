from abjad import *


def test_NamedChromaticPitchClassSegment_retrograde_01():

    npc_segment_1 = pitchtools.NamedChromaticPitchClassSegment([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),
        pitchtools.NamedChromaticPitchClass('f'),
        pitchtools.NamedChromaticPitchClass('g'),])

    npc_segment_2 = pitchtools.NamedChromaticPitchClassSegment([
        pitchtools.NamedChromaticPitchClass('g'),
        pitchtools.NamedChromaticPitchClass('f'),
        pitchtools.NamedChromaticPitchClass('e'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('c'),])

    assert npc_segment_1.retrograde() == npc_segment_2
    assert npc_segment_2.retrograde() == npc_segment_1
