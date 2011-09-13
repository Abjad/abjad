from abjad import *


def test_pitchtools_chromatic_pitch_name_to_diatonic_pitch_name_01():

    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_name("c''") == "c''"
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_name("cs''") == "c''"
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_name("d''") == "d''"
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_name("ef''") == "e''"
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_name("e''") == "e''"
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_name("f''") == "f''"
