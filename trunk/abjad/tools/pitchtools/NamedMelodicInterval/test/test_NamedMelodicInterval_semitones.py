# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval_semitones_01():

    assert pitchtools.NamedMelodicInterval('perfect', 1).semitones == 0
    assert pitchtools.NamedMelodicInterval('minor', 2).semitones == 1
    assert pitchtools.NamedMelodicInterval('major', 2).semitones == 2
    assert pitchtools.NamedMelodicInterval('minor', 3).semitones == 3
    assert pitchtools.NamedMelodicInterval('major', 3).semitones == 4
    assert pitchtools.NamedMelodicInterval('perfect', 4).semitones == 5
    assert pitchtools.NamedMelodicInterval('augmented', 4).semitones == 6
    assert pitchtools.NamedMelodicInterval('diminished', 5).semitones == 6
    assert pitchtools.NamedMelodicInterval('perfect', 5).semitones == 7
    assert pitchtools.NamedMelodicInterval('minor', 6).semitones == 8
    assert pitchtools.NamedMelodicInterval('major', 6).semitones == 9
    assert pitchtools.NamedMelodicInterval('minor', 7).semitones == 10
    assert pitchtools.NamedMelodicInterval('major', 7).semitones == 11
    assert pitchtools.NamedMelodicInterval('perfect', 8).semitones == 12


def test_NamedMelodicInterval_semitones_02():

    assert pitchtools.NamedMelodicInterval('major', 23).semitones == 38
    assert pitchtools.NamedMelodicInterval('major', -23).semitones == -38
