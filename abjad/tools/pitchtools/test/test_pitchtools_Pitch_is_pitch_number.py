# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Pitch_is_pitch_number_01():

    assert pitchtools.Pitch.is_pitch_number(-99)
    assert pitchtools.Pitch.is_pitch_number(-98.5)
    assert pitchtools.Pitch.is_pitch_number(-1)
    assert pitchtools.Pitch.is_pitch_number(-0.5)
    assert pitchtools.Pitch.is_pitch_number(0)
    assert pitchtools.Pitch.is_pitch_number(0.5)
    assert pitchtools.Pitch.is_pitch_number(1)
    assert pitchtools.Pitch.is_pitch_number(98.5)
    assert pitchtools.Pitch.is_pitch_number(99)


def test_pitchtools_Pitch_is_pitch_number_02():

    assert not pitchtools.Pitch.is_pitch_number(1.6)
    assert not pitchtools.Pitch.is_pitch_number('foo')
