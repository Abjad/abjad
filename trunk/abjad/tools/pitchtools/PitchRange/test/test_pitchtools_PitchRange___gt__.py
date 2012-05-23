from abjad import *


def test_pitchtools_PitchRange___gt___01():

    pitch_range = pitchtools.PitchRange(-39, 48)

    assert -99 < pitch_range
    assert not -39 < pitch_range
    assert not 0 < pitch_range
    assert not 48 < pitch_range
    assert not 99 < pitch_range


def test_pitchtools_PitchRange___gt___02():

    pitch_range = pitchtools.PitchRange(-39, 48)

    assert pitchtools.NamedChromaticPitch(-99) < pitch_range
    assert not pitchtools.NamedChromaticPitch(-39) < pitch_range
    assert not pitchtools.NamedChromaticPitch(0) < pitch_range
    assert not pitchtools.NamedChromaticPitch(48) < pitch_range
    assert not pitchtools.NamedChromaticPitch(99) < pitch_range
