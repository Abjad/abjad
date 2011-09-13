from abjad import *


def test_pitchtools_is_octave_tick_string_01():

    assert pitchtools.is_octave_tick_string(',,,')
    assert pitchtools.is_octave_tick_string(',,')
    assert pitchtools.is_octave_tick_string(',')
    assert pitchtools.is_octave_tick_string('')
    assert pitchtools.is_octave_tick_string("")
    assert pitchtools.is_octave_tick_string("'")
    assert pitchtools.is_octave_tick_string("''")
    assert pitchtools.is_octave_tick_string("'''")


def test_pitchtools_is_octave_tick_string_02():

    assert not pitchtools.is_octave_tick_string('foo')
    assert not pitchtools.is_octave_tick_string(8)
