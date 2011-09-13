from abjad import *


def test_HarmonicDiatonicInterval_semitones_01():

    assert pitchtools.HarmonicDiatonicInterval('perfect', 1).semitones == 0
    assert pitchtools.HarmonicDiatonicInterval('minor', 2).semitones == 1
    assert pitchtools.HarmonicDiatonicInterval('major', 2).semitones == 2
    assert pitchtools.HarmonicDiatonicInterval('minor', 3).semitones == 3
    assert pitchtools.HarmonicDiatonicInterval('major', 3).semitones == 4
    assert pitchtools.HarmonicDiatonicInterval('perfect', 4).semitones == 5
    assert pitchtools.HarmonicDiatonicInterval('augmented', 4).semitones == 6
    assert pitchtools.HarmonicDiatonicInterval('diminished', 5).semitones == 6
    assert pitchtools.HarmonicDiatonicInterval('perfect', 5).semitones == 7
    assert pitchtools.HarmonicDiatonicInterval('minor', 6).semitones == 8
    assert pitchtools.HarmonicDiatonicInterval('major', 6).semitones == 9
    assert pitchtools.HarmonicDiatonicInterval('minor', 7).semitones == 10
    assert pitchtools.HarmonicDiatonicInterval('major', 7).semitones == 11
    assert pitchtools.HarmonicDiatonicInterval('perfect', 8).semitones == 12


def test_HarmonicDiatonicInterval_semitones_02():

    assert pitchtools.HarmonicDiatonicInterval('major', 23).semitones == 38
    assert pitchtools.HarmonicDiatonicInterval('major', -23).semitones == 38
