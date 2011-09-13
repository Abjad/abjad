from abjad import *


def test_pitchtools_diatonic_pitch_class_number_to_diatonic_pitch_class_name_01():

    assert pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(0) == 'c'
    assert pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(1) == 'd'
    assert pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(2) == 'e'
    assert pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(3) == 'f'
    assert pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(4) == 'g'
    assert pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(5) == 'a'
    assert pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(6) == 'b'
