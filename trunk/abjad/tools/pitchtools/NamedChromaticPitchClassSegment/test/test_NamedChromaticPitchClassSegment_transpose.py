from abjad import *


def test_NamedChromaticPitchClassSegment_transpose_01():

    npc_segment_1 = pitchtools.NamedChromaticPitchClassSegment([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),
        pitchtools.NamedChromaticPitchClass('f'),
        pitchtools.NamedChromaticPitchClass('g'),])

    npc_segment_2 = pitchtools.NamedChromaticPitchClassSegment([
        pitchtools.NamedChromaticPitchClass('df'),
        pitchtools.NamedChromaticPitchClass('ef'),
        pitchtools.NamedChromaticPitchClass('f'),
        pitchtools.NamedChromaticPitchClass('gf'),
        pitchtools.NamedChromaticPitchClass('af'),])

    minor_second_ascending = pitchtools.MelodicDiatonicInterval('minor', 2)
    assert npc_segment_1.transpose(minor_second_ascending) == npc_segment_2

    major_seventh_descending = pitchtools.MelodicDiatonicInterval('major', -7)
    assert npc_segment_1.transpose(major_seventh_descending) == npc_segment_2

    minor_second_descending = pitchtools.MelodicDiatonicInterval('minor', -2)
    assert npc_segment_2.transpose(minor_second_descending) == npc_segment_1

    major_seventh_ascending = pitchtools.MelodicDiatonicInterval('major', 7)
    assert npc_segment_2.transpose(major_seventh_ascending) == npc_segment_1
