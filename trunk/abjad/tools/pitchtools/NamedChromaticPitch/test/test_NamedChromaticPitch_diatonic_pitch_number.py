from abjad import *


def test_NamedChromaticPitch_diatonic_pitch_number_01():

    assert pitchtools.NamedChromaticPitch("cs''").diatonic_pitch_number == 7
