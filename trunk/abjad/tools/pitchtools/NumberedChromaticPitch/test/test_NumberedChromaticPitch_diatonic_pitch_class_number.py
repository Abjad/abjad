from abjad import *


def test_NumberedChromaticPitch_diatonic_pitch_class_number_01():

    assert pitchtools.NumberedChromaticPitch(11).diatonic_pitch_class_number == 6
    assert pitchtools.NumberedChromaticPitch(12).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedChromaticPitch(13).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedChromaticPitch(14).diatonic_pitch_class_number == 1
    assert pitchtools.NumberedChromaticPitch(15).diatonic_pitch_class_number == 2
