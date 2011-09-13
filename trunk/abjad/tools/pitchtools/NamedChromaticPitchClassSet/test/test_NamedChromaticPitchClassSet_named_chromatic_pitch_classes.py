from abjad import *


def test_NamedChromaticPitchClassSet_named_chromatic_pitch_classes_01():

    npc_set = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),])
    pitch_classes = npc_set.named_chromatic_pitch_classes

    assert isinstance(pitch_classes, tuple)

    assert pitch_classes[0] == pitchtools.NamedChromaticPitchClass('c')
    assert pitch_classes[1] == pitchtools.NamedChromaticPitchClass('d')
    assert pitch_classes[2] == pitchtools.NamedChromaticPitchClass('e')
