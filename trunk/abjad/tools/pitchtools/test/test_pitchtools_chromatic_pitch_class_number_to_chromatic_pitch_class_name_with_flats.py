from abjad import *


def test_pitchtools_chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats_01():

    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(0) == 'c'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(0.5) == 'dtqf'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(1) == 'df'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(1.5) == 'dqf'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(2) == 'd'
    assert pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(2.5) == 'etqf'
