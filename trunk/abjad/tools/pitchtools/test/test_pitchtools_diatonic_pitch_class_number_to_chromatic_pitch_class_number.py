from abjad import *


def test_pitchtools_diatonic_pitch_class_number_to_chromatic_pitch_class_number_01():

    assert pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(0) == 0
    assert pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(1) == 2
    assert pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(2) == 4
    assert pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(3) == 5
    assert pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(4) == 7
    assert pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(5) == 9
    assert pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number(6) == 11
