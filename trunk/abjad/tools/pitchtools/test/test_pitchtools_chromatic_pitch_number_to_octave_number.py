from abjad import *


def test_pitchtools_chromatic_pitch_number_to_octave_number_01():

    assert pitchtools.chromatic_pitch_number_to_octave_number(-12) == 3
    assert pitchtools.chromatic_pitch_number_to_octave_number(-11) == 3
    assert pitchtools.chromatic_pitch_number_to_octave_number(0) == 4
    assert pitchtools.chromatic_pitch_number_to_octave_number(1) == 4
    assert pitchtools.chromatic_pitch_number_to_octave_number(12) == 5
    assert pitchtools.chromatic_pitch_number_to_octave_number(13) == 5
