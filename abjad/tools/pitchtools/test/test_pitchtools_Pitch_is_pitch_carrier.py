# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Pitch_is_pitch_carrier_01():

    assert pitchtools.Pitch.is_pitch_carrier(NamedPitch(0))
    assert pitchtools.Pitch.is_pitch_carrier(Note("c'4"))
    assert pitchtools.Pitch.is_pitch_carrier(scoretools.NoteHead(client=None, written_pitch=0))
    assert pitchtools.Pitch.is_pitch_carrier(Chord([0, 2, 11], (1, 4)))


def test_pitchtools_Pitch_is_pitch_carrier_02():

    assert not pitchtools.Pitch.is_pitch_carrier(Staff([]))
    assert not pitchtools.Pitch.is_pitch_carrier(Voice([]))
    assert not pitchtools.Pitch.is_pitch_carrier(0)
    assert not pitchtools.Pitch.is_pitch_carrier('foo')
