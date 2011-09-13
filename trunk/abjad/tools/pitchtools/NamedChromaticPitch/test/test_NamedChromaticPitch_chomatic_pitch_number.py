from abjad import *


def test_NamedChromaticPitch_chomatic_pitch_number_01():

    assert pitchtools.NamedChromaticPitch("cs''").chromatic_pitch_number == 13
