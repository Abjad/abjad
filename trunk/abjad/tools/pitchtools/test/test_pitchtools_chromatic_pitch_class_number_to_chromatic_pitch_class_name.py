from abjad import *


def test_pitchtools_chromatic_pitch_class_number_to_chromatic_pitch_class_name_01():

    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(0) == 'c'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(0.5) == 'cqs'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(1) == 'cs'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(1.5) == 'dqf'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(2) == 'd'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(2.5) == 'dqs'
