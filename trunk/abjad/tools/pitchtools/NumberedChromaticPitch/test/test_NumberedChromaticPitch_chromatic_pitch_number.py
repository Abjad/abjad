from abjad import *


def test_NumberedChromaticPitch_chromatic_pitch_number_01():

    assert pitchtools.NumberedChromaticPitch(-14).chromatic_pitch_number == -14
    assert pitchtools.NumberedChromaticPitch(14).chromatic_pitch_number == 14
    assert pitchtools.NumberedChromaticPitch(-2).chromatic_pitch_number == -2
    assert pitchtools.NumberedChromaticPitch(2).chromatic_pitch_number == 2
