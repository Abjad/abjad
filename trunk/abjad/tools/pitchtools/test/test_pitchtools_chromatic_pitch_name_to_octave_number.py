from abjad import *


def test_pitchtools_chromatic_pitch_name_to_octave_number_01():

    assert pitchtools.chromatic_pitch_name_to_octave_number("cs'") == 4
    assert pitchtools.chromatic_pitch_name_to_octave_number('cs') == 3
    assert pitchtools.chromatic_pitch_name_to_octave_number('cs,') == 2
