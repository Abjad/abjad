from abjad import *


def test_pitchtools_diatonic_pitch_number_to_diatonic_pitch_class_number_01():

    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(-1) == 6
    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(0) == 0
    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(6) == 6
    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number(7) == 0
