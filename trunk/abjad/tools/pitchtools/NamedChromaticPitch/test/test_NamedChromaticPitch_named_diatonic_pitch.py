from abjad import *


def test_NamedChromaticPitch_named_diatonic_pitch_01():

    assert pitchtools.NamedChromaticPitch("cf''").named_diatonic_pitch == \
        pitchtools.NamedDiatonicPitch("c''")

    assert pitchtools.NamedChromaticPitch("cqf''").named_diatonic_pitch == \
        pitchtools.NamedDiatonicPitch("c''")

    assert pitchtools.NamedChromaticPitch("c''").named_diatonic_pitch == \
        pitchtools.NamedDiatonicPitch("c''")

    assert pitchtools.NamedChromaticPitch("cqs''").named_diatonic_pitch == \
        pitchtools.NamedDiatonicPitch("c''")

    assert pitchtools.NamedChromaticPitch("cs''").named_diatonic_pitch == \
        pitchtools.NamedDiatonicPitch("c''")
