from abjad import *


def test_NamedChromaticPitch_numbered_diatonic_pitch_class_01():

    assert pitchtools.NamedChromaticPitch("c''").numbered_diatonic_pitch_class == 0
    assert pitchtools.NamedChromaticPitch("cs''").numbered_diatonic_pitch_class == 0
    assert pitchtools.NamedChromaticPitch("d''").numbered_diatonic_pitch_class == 1
    assert pitchtools.NamedChromaticPitch("ef''").numbered_diatonic_pitch_class == 2
    assert pitchtools.NamedChromaticPitch("e''").numbered_diatonic_pitch_class == 2
    assert pitchtools.NamedChromaticPitch("f''").numbered_diatonic_pitch_class == 3
    assert pitchtools.NamedChromaticPitch("fs''").numbered_diatonic_pitch_class == 3
    assert pitchtools.NamedChromaticPitch("g''").numbered_diatonic_pitch_class == 4
    assert pitchtools.NamedChromaticPitch("af''").numbered_diatonic_pitch_class == 5
    assert pitchtools.NamedChromaticPitch("a''").numbered_diatonic_pitch_class == 5
    assert pitchtools.NamedChromaticPitch("bf''").numbered_diatonic_pitch_class == 6
    assert pitchtools.NamedChromaticPitch("b''").numbered_diatonic_pitch_class == 6
