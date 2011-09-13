from abjad import *


def test_NamedChromaticPitchClassSet_transpose_01():

    npc_set_1 = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),])

    npc_set_2 = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('df'),
        pitchtools.NamedChromaticPitchClass('ef'),
        pitchtools.NamedChromaticPitchClass('f'),])

    minor_second_ascending = pitchtools.MelodicDiatonicInterval('minor', 2)
    assert npc_set_1.transpose(minor_second_ascending) == npc_set_2

    major_seventh_descending = pitchtools.MelodicDiatonicInterval('major', -7)
    assert npc_set_1.transpose(major_seventh_descending) == npc_set_2

    minor_second_descending = pitchtools.MelodicDiatonicInterval('minor', -2)
    assert npc_set_2.transpose(minor_second_descending) == npc_set_1

    major_seventh_ascending = pitchtools.MelodicDiatonicInterval('major', 7)
    assert npc_set_2.transpose(major_seventh_ascending) == npc_set_1
