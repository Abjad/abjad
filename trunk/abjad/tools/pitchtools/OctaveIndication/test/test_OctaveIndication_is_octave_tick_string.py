# -*- encoding: utf-8 -*-
from abjad import *


def test_OctaveIndication_is_octave_tick_string_01():

    assert pitchtools.OctaveIndication.is_octave_tick_string(',,,')
    assert pitchtools.OctaveIndication.is_octave_tick_string(',,')
    assert pitchtools.OctaveIndication.is_octave_tick_string(',')
    assert pitchtools.OctaveIndication.is_octave_tick_string('')
    assert pitchtools.OctaveIndication.is_octave_tick_string("")
    assert pitchtools.OctaveIndication.is_octave_tick_string("'")
    assert pitchtools.OctaveIndication.is_octave_tick_string("''")
    assert pitchtools.OctaveIndication.is_octave_tick_string("'''")


def test_OctaveIndication_is_octave_tick_string_02():

    assert not pitchtools.OctaveIndication.is_octave_tick_string('foo')
    assert not pitchtools.OctaveIndication.is_octave_tick_string(8)
