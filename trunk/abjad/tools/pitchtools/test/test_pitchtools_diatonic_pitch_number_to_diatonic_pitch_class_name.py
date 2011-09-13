from abjad import *


def test_pitchtools_diatonic_pitch_number_to_diatonic_pitch_class_name_01():

    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name(-1) == 'b'
    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name(0) == 'c'
    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name(6) == 'b'
    assert pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_name(7) == 'c'
