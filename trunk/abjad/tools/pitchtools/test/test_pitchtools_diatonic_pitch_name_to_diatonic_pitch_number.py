from abjad import *


def test_pitchtools_diatonic_pitch_name_to_diatonic_pitch_number_01():

    assert pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("b") == -1
    assert pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("c'") == 0
    assert pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("b'") == 6
    assert pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("c''") == 7
    assert pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("b''") == 13
    assert pitchtools.diatonic_pitch_name_to_diatonic_pitch_number("c'''") == 14
