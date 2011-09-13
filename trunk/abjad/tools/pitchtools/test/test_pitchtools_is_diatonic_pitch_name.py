from abjad import *


def test_pitchtools_is_diatonic_pitch_name_01():

    assert pitchtools.is_diatonic_pitch_name("c,,,")
    assert pitchtools.is_diatonic_pitch_name("c,,")
    assert pitchtools.is_diatonic_pitch_name("c,")
    assert pitchtools.is_diatonic_pitch_name("c")
    assert pitchtools.is_diatonic_pitch_name("c'")
    assert pitchtools.is_diatonic_pitch_name("c'")
    assert pitchtools.is_diatonic_pitch_name("c''")


def test_pitchtools_is_diatonic_pitch_name_02():

    assert not pitchtools.is_diatonic_pitch_name('cs')
    assert not pitchtools.is_diatonic_pitch_name(7)
    assert not pitchtools.is_diatonic_pitch_name(7.0)
