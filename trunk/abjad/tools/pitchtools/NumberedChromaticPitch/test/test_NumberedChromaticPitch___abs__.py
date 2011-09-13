from abjad import *


def test_NumberedChromaticPitch___abs___01():

    assert abs(pitchtools.NumberedChromaticPitch(11)) == 11
    assert abs(pitchtools.NumberedChromaticPitch(11.5)) == 11.5
    assert abs(pitchtools.NumberedChromaticPitch(13)) == 13
    assert abs(pitchtools.NumberedChromaticPitch(13.5)) == 13.5
