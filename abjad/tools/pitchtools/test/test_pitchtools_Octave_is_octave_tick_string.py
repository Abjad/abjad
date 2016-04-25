# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Octave_is_octave_tick_string_01():

    assert pitchtools.Octave.is_octave_tick_string(',,,')
    assert pitchtools.Octave.is_octave_tick_string(',,')
    assert pitchtools.Octave.is_octave_tick_string(',')
    assert pitchtools.Octave.is_octave_tick_string('')
    assert pitchtools.Octave.is_octave_tick_string("")
    assert pitchtools.Octave.is_octave_tick_string("'")
    assert pitchtools.Octave.is_octave_tick_string("''")
    assert pitchtools.Octave.is_octave_tick_string("'''")


def test_pitchtools_Octave_is_octave_tick_string_02():

    assert not pitchtools.Octave.is_octave_tick_string('foo')
    assert not pitchtools.Octave.is_octave_tick_string(8)
