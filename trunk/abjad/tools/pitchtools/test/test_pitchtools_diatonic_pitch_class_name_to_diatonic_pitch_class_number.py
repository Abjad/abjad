from abjad import *


def test_pitchtools_diatonic_pitch_class_name_to_diatonic_pitch_class_number_01():

    assert pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('c') == 0
    assert pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('d') == 1
    assert pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('e') == 2
    assert pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('f') == 3
    assert pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('g') == 4
    assert pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('a') == 5
    assert pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('b') == 6
