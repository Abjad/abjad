from abjad import *


def test_pitchtools_chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps_01():

    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(0) == 'c'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(0.5) == 'cqs'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(1) == 'cs'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(1.5) == 'ctqs'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(2) == 'd'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(2.5) == 'dqs'
