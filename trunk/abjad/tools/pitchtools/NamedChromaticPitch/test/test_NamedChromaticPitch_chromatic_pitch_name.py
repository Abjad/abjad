from abjad import *


def test_NamedChromaticPitch_chromatic_pitch_name_01():

    assert pitchtools.NamedChromaticPitch("cs''").chromatic_pitch_name == "cs''"
