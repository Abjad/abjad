from abjad import *


def test_pitchtools_chromatic_pitch_name_to_chromatic_pitch_number_01():

    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("cff''") == 10
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("ctqf''") == 10.5
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("cf''") == 11
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("cqf''") == 11.5
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("c''") == 12
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("cqs''") == 12.5
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("cs''") == 13
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("ctqs''") == 13.5
    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("css''") == 14

    assert pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("d''") == 14
