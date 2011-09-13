from abjad import *


def test_pitchtools_chromatic_pitch_name_to_chromatic_pitch_class_number_01():

    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("cf''") == 11
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("c''") == 0
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("cs''") == 1
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("bf''") == 10
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("b''") == 11
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number("bs''") == 0
