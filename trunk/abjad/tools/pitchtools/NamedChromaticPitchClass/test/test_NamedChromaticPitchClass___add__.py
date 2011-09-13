from abjad import *


def test_NamedChromaticPitchClass___add___01():

    npc = pitchtools.NamedChromaticPitchClass('c')

    new = npc + pitchtools.MelodicDiatonicInterval('perfect', 1)
    new == pitchtools.NamedChromaticPitchClass('c')

    new = npc + pitchtools.MelodicDiatonicInterval('minor', 2)
    new == pitchtools.NamedChromaticPitchClass('df')

    new = npc + pitchtools.MelodicDiatonicInterval('minor', -2)
    new == pitchtools.NamedChromaticPitchClass('b')

    new = npc + pitchtools.MelodicDiatonicInterval('major', 2)
    new == pitchtools.NamedChromaticPitchClass('d')

    new = npc + pitchtools.MelodicDiatonicInterval('major', -2)
    new == pitchtools.NamedChromaticPitchClass('bf')
