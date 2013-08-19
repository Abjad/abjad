# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval_semitones_01():

    assert pitchtools.NamedHarmonicInterval('perfect', 1).semitones == 0
    assert pitchtools.NamedHarmonicInterval('minor', 2).semitones == 1
    assert pitchtools.NamedHarmonicInterval('major', 2).semitones == 2
    assert pitchtools.NamedHarmonicInterval('minor', 3).semitones == 3
    assert pitchtools.NamedHarmonicInterval('major', 3).semitones == 4
    assert pitchtools.NamedHarmonicInterval('perfect', 4).semitones == 5
    assert pitchtools.NamedHarmonicInterval('augmented', 4).semitones == 6
    assert pitchtools.NamedHarmonicInterval('diminished', 5).semitones == 6
    assert pitchtools.NamedHarmonicInterval('perfect', 5).semitones == 7
    assert pitchtools.NamedHarmonicInterval('minor', 6).semitones == 8
    assert pitchtools.NamedHarmonicInterval('major', 6).semitones == 9
    assert pitchtools.NamedHarmonicInterval('minor', 7).semitones == 10
    assert pitchtools.NamedHarmonicInterval('major', 7).semitones == 11
    assert pitchtools.NamedHarmonicInterval('perfect', 8).semitones == 12


def test_NamedHarmonicInterval_semitones_02():

    assert pitchtools.NamedHarmonicInterval('major', 23).semitones == 38
    assert pitchtools.NamedHarmonicInterval('major', -23).semitones == 38
