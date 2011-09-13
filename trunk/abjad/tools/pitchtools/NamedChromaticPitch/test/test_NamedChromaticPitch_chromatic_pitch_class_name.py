from abjad import *


def test_NamedChromaticPitch_chromatic_pitch_class_name_01():

    assert pitchtools.NamedChromaticPitch("cs''").chromatic_pitch_class_number == 1
