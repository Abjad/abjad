from abjad import *


def test_pitchtools_PitchRange___lt___01():

    pitch_range = pitchtools.PitchRange(-39, 48)

    assert not pitch_range < -99
    assert not pitch_range < -39
    assert not pitch_range < 0
    assert not pitch_range < 48
    assert pitch_range < 99


def test_pitchtools_PitchRange___lt___02():

    pitch_range = pitchtools.PitchRange(-39, 48)

    assert not pitch_range < pitchtools.NamedChromaticPitch(-99)
    assert not pitch_range < pitchtools.NamedChromaticPitch(-39)
    assert not pitch_range < pitchtools.NamedChromaticPitch(0)
    assert not pitch_range < pitchtools.NamedChromaticPitch(48)
    assert pitch_range < pitchtools.NamedChromaticPitch(99)
