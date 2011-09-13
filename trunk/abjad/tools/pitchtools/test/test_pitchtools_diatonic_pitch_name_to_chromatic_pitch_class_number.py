from abjad import *


def test_pitchtools_diatonic_pitch_name_to_chromatic_pitch_class_number_01():

    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("c''") == 0
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("d''") == 2
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("e''") == 4
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("f''") == 5
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("g''") == 7
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("a''") == 9
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_number("b''") == 11
