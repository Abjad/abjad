from abjad import *


def test_NamedChromaticPitch_diatonic_pitch_class_number_01():

    assert pitchtools.NamedChromaticPitch("cs''").diatonic_pitch_class_number == 0
