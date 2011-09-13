from abjad import *


def test_pitchtools_chromatic_pitch_number_to_chromatic_pitch_name_01():

    assert pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(13, 'mixed') == "cs''"
    assert pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(14, 'mixed') == "d''"
    assert pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(15, 'mixed') == "ef''"
    assert pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(16, 'mixed') == "e''"
    assert pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(17, 'mixed') == "f''"
