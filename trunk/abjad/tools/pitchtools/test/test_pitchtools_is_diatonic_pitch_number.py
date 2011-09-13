from abjad import *


def test_pitchtools_is_diatonic_pitch_number_01():

    assert pitchtools.is_diatonic_pitch_number(-99)
    assert pitchtools.is_diatonic_pitch_number(-1)
    assert pitchtools.is_diatonic_pitch_number(0)
    assert pitchtools.is_diatonic_pitch_number(1)
    assert pitchtools.is_diatonic_pitch_number(99)


def test_pitchtools_is_diatonic_pitch_number_02():

    assert not pitchtools.is_diatonic_pitch_number('foo')
