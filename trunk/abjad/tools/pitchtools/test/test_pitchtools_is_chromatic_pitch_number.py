from abjad import *


def test_pitchtools_is_chromatic_pitch_number_01():

    assert pitchtools.is_chromatic_pitch_number(-99)
    assert pitchtools.is_chromatic_pitch_number(-98.5)
    assert pitchtools.is_chromatic_pitch_number(-1)
    assert pitchtools.is_chromatic_pitch_number(-0.5)
    assert pitchtools.is_chromatic_pitch_number(0)
    assert pitchtools.is_chromatic_pitch_number(0.5)
    assert pitchtools.is_chromatic_pitch_number(1)
    assert pitchtools.is_chromatic_pitch_number(98.5)
    assert pitchtools.is_chromatic_pitch_number(99)


def test_pitchtools_is_chromatic_pitch_number_02():

    assert not pitchtools.is_chromatic_pitch_number(1.6)
    assert not pitchtools.is_chromatic_pitch_number('foo')
