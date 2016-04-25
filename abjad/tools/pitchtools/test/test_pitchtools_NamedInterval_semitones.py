# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval_semitones_01():

    assert pitchtools.NamedInterval('perfect', 1).semitones == 0
    assert pitchtools.NamedInterval('minor', 2).semitones == 1
    assert pitchtools.NamedInterval('major', 2).semitones == 2
    assert pitchtools.NamedInterval('minor', 3).semitones == 3
    assert pitchtools.NamedInterval('major', 3).semitones == 4
    assert pitchtools.NamedInterval('perfect', 4).semitones == 5
    assert pitchtools.NamedInterval('augmented', 4).semitones == 6
    assert pitchtools.NamedInterval('diminished', 5).semitones == 6
    assert pitchtools.NamedInterval('perfect', 5).semitones == 7
    assert pitchtools.NamedInterval('minor', 6).semitones == 8
    assert pitchtools.NamedInterval('major', 6).semitones == 9
    assert pitchtools.NamedInterval('minor', 7).semitones == 10
    assert pitchtools.NamedInterval('major', 7).semitones == 11
    assert pitchtools.NamedInterval('perfect', 8).semitones == 12


def test_pitchtools_NamedInterval_semitones_02():

    assert pitchtools.NamedInterval('major', 23).semitones == 38
    assert pitchtools.NamedInterval('major', -23).semitones == -38
