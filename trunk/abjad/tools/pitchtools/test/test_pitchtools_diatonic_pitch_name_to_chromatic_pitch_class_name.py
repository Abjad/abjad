from abjad import *


def test_pitchtools_diatonic_pitch_name_to_chromatic_pitch_class_name_01():

    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_name("c'") == 'c'
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_name("c") == 'c'
    assert pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_name("c,") == 'c'
