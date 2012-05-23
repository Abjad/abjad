from abjad import *


def test_NumberedDiatonicPitch_chromatic_pitch_number_01():

    assert pitchtools.NumberedDiatonicPitch(6).chromatic_pitch_number == 11
    assert pitchtools.NumberedDiatonicPitch(7).chromatic_pitch_number == 12
    assert pitchtools.NumberedDiatonicPitch(8).chromatic_pitch_number == 14
    assert pitchtools.NumberedDiatonicPitch(9).chromatic_pitch_number == 16
