from abjad import *


def test_pitchtools_diatonic_pitch_number_to_chromatic_pitch_number_01():

    assert pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(6) == 11
    assert pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(7) == 12
    assert pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(8) == 14
    assert pitchtools.diatonic_pitch_number_to_chromatic_pitch_number(9) == 16
