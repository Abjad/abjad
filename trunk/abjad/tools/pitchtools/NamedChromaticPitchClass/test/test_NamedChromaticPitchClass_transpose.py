from abjad import *


def test_NamedChromaticPitchClass_transpose_01():

    npc = pitchtools.NamedChromaticPitchClass('c')

    new = npc.transpose(pitchtools.MelodicDiatonicInterval('perfect', 1))
    new == pitchtools.NamedChromaticPitchClass('c')

    new = npc.transpose(pitchtools.MelodicDiatonicInterval('minor', 2))
    new == pitchtools.NamedChromaticPitchClass('df')

    new = npc.transpose(pitchtools.MelodicDiatonicInterval('minor', -2))
    new == pitchtools.NamedChromaticPitchClass('b')

    new = npc.transpose(pitchtools.MelodicDiatonicInterval('major', 2))
    new == pitchtools.NamedChromaticPitchClass('d')

    new = npc.transpose(pitchtools.MelodicDiatonicInterval('major', -2))
    new == pitchtools.NamedChromaticPitchClass('bf')
