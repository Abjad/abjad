from abjad import *


def test_pitchtools_chromatic_pitch_number_to_diatonic_pitch_number_01():

    assert pitchtools.chromatic_pitch_number_to_diatonic_pitch_number(11) == 6
    assert pitchtools.chromatic_pitch_number_to_diatonic_pitch_number(12) == 7
    assert pitchtools.chromatic_pitch_number_to_diatonic_pitch_number(13) == 7
    assert pitchtools.chromatic_pitch_number_to_diatonic_pitch_number(14) == 8
    assert pitchtools.chromatic_pitch_number_to_diatonic_pitch_number(15) == 9
