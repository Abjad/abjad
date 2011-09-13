from abjad import *


def test_NamedChromaticPitch_diatonic_pitch_name_01():

    assert pitchtools.NamedChromaticPitch("cs''").diatonic_pitch_name == "c''"
