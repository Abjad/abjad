from abjad import *


def test_pitchtools_chromatic_pitch_name_to_diatonic_pitch_class_name_01():

    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name("c''") == 'c'
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name("cs''") == 'c'
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name("d''") == 'd'
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name("ef''") == 'e'
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name("e''") == 'e'
    assert pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name("f''") == 'f'
