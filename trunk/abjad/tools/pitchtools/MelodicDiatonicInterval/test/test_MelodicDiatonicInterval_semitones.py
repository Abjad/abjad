from abjad import *


def test_MelodicDiatonicInterval_semitones_01():

    assert pitchtools.MelodicDiatonicInterval('perfect', 1).semitones == 0
    assert pitchtools.MelodicDiatonicInterval('minor', 2).semitones == 1
    assert pitchtools.MelodicDiatonicInterval('major', 2).semitones == 2
    assert pitchtools.MelodicDiatonicInterval('minor', 3).semitones == 3
    assert pitchtools.MelodicDiatonicInterval('major', 3).semitones == 4
    assert pitchtools.MelodicDiatonicInterval('perfect', 4).semitones == 5
    assert pitchtools.MelodicDiatonicInterval('augmented', 4).semitones == 6
    assert pitchtools.MelodicDiatonicInterval('diminished', 5).semitones == 6
    assert pitchtools.MelodicDiatonicInterval('perfect', 5).semitones == 7
    assert pitchtools.MelodicDiatonicInterval('minor', 6).semitones == 8
    assert pitchtools.MelodicDiatonicInterval('major', 6).semitones == 9
    assert pitchtools.MelodicDiatonicInterval('minor', 7).semitones == 10
    assert pitchtools.MelodicDiatonicInterval('major', 7).semitones == 11
    assert pitchtools.MelodicDiatonicInterval('perfect', 8).semitones == 12


def test_MelodicDiatonicInterval_semitones_02():

    assert pitchtools.MelodicDiatonicInterval('major', 23).semitones == 38
    assert pitchtools.MelodicDiatonicInterval('major', -23).semitones == -38
