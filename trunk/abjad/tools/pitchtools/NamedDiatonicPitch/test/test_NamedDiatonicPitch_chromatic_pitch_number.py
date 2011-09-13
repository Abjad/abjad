from abjad import *


def test_NamedDiatonicPitch_chromatic_pitch_number_01():

    assert pitchtools.NamedDiatonicPitch("c''").chromatic_pitch_number == 12
    assert pitchtools.NamedDiatonicPitch("d''").chromatic_pitch_number == 14
    assert pitchtools.NamedDiatonicPitch("e''").chromatic_pitch_number == 16
    assert pitchtools.NamedDiatonicPitch("f''").chromatic_pitch_number == 17
