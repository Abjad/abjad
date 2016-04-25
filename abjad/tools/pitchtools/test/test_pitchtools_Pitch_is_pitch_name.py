# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Pitch_is_pitch_name_01():

    assert pitchtools.Pitch.is_pitch_name('c,')
    assert pitchtools.Pitch.is_pitch_name('cs,')
    assert pitchtools.Pitch.is_pitch_name('c')
    assert pitchtools.Pitch.is_pitch_name('cs')
    assert pitchtools.Pitch.is_pitch_name("ctqs''")


def test_pitchtools_Pitch_is_pitch_name_02():

    assert not pitchtools.Pitch.is_pitch_name('foo')
    assert not pitchtools.Pitch.is_pitch_name('c4')
