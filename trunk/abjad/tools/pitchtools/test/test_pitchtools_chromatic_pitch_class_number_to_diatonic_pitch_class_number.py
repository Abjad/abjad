from abjad import *


def test_pitchtools_chromatic_pitch_class_number_to_diatonic_pitch_class_number_01():

    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(0) == 0
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(1) == 0
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(2) == 1
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(3) == 2
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(4) == 2
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(5) == 3
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(6) == 3
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(7) == 4
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(8) == 5
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(9) == 5
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(10) == 6
    assert pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(11) == 6
