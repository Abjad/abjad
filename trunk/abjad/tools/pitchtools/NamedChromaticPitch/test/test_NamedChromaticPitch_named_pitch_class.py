from abjad import *


def test_NamedChromaticPitch_named_pitch_class_01():

    pitch = pitchtools.NamedChromaticPitch('cs', 4)
    assert pitch.named_chromatic_pitch_class == pitchtools.NamedChromaticPitchClass('cs')
