from abjad import *


def test_NamedChromaticPitchClass_numbered_chromatic_pitch_class_01():

    npc = pitchtools.NamedChromaticPitchClass('c')
    assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(0)

    npc = pitchtools.NamedChromaticPitchClass('cs')
    assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(1)

    npc = pitchtools.NamedChromaticPitchClass('cf')
    assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(11)

    npc = pitchtools.NamedChromaticPitchClass('cqs')
    assert npc.numbered_chromatic_pitch_class == pitchtools.NumberedChromaticPitchClass(0.5)
