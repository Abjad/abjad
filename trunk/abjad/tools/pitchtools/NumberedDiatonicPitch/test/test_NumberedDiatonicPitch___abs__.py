from abjad import *


def test_NumberedDiatonicPitch___abs___01():

    assert abs(pitchtools.NumberedDiatonicPitch(-1)) == -1
    assert abs(pitchtools.NumberedDiatonicPitch(0)) == 0
    assert abs(pitchtools.NumberedDiatonicPitch(6)) == 6
    assert abs(pitchtools.NumberedDiatonicPitch(7)) == 7
    assert abs(pitchtools.NumberedDiatonicPitch(13)) == 13
    assert abs(pitchtools.NumberedDiatonicPitch(14)) == 14
