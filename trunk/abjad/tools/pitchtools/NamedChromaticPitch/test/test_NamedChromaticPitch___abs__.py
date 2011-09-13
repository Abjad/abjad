from abjad import *


def test_NamedChromaticPitch___abs___01():

    assert abs(pitchtools.NamedChromaticPitch(11)) == 11
    assert abs(pitchtools.NamedChromaticPitch(11.5)) == 11.5
    assert abs(pitchtools.NamedChromaticPitch(13)) == 13
    assert abs(pitchtools.NamedChromaticPitch(13.5)) == 13.5
