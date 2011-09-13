from abjad import *


def test_HarmonicDiatonicInterval_staff_spaces_01():

    assert pitchtools.HarmonicDiatonicInterval('perfect', 1).staff_spaces == 0
    assert pitchtools.HarmonicDiatonicInterval('minor', 2).staff_spaces == 1
    assert pitchtools.HarmonicDiatonicInterval('major', 2).staff_spaces == 1
    assert pitchtools.HarmonicDiatonicInterval('minor', 3).staff_spaces == 2
    assert pitchtools.HarmonicDiatonicInterval('major', 3).staff_spaces == 2
    assert pitchtools.HarmonicDiatonicInterval('perfect', 4).staff_spaces == 3
    assert pitchtools.HarmonicDiatonicInterval('augmented', 4).staff_spaces == 3
    assert pitchtools.HarmonicDiatonicInterval('diminished', 5).staff_spaces == 4
    assert pitchtools.HarmonicDiatonicInterval('perfect', 5).staff_spaces == 4
    assert pitchtools.HarmonicDiatonicInterval('minor', 6).staff_spaces == 5
    assert pitchtools.HarmonicDiatonicInterval('major', 6).staff_spaces == 5
    assert pitchtools.HarmonicDiatonicInterval('minor', 7).staff_spaces == 6
    assert pitchtools.HarmonicDiatonicInterval('major', 7).staff_spaces == 6
    assert pitchtools.HarmonicDiatonicInterval('perfect', 8).staff_spaces == 7


def test_HarmonicDiatonicInterval_staff_spaces_02():

    assert pitchtools.HarmonicDiatonicInterval('perfect', -1).staff_spaces == 0
    assert pitchtools.HarmonicDiatonicInterval('minor', -2).staff_spaces == 1
    assert pitchtools.HarmonicDiatonicInterval('major', -2).staff_spaces == 1
    assert pitchtools.HarmonicDiatonicInterval('minor', -3).staff_spaces == 2
    assert pitchtools.HarmonicDiatonicInterval('major', -3).staff_spaces == 2
    assert pitchtools.HarmonicDiatonicInterval('perfect', -4).staff_spaces == 3
    assert pitchtools.HarmonicDiatonicInterval('augmented', -4).staff_spaces == 3
    assert pitchtools.HarmonicDiatonicInterval('diminished', -5).staff_spaces == 4
    assert pitchtools.HarmonicDiatonicInterval('perfect', -5).staff_spaces == 4
    assert pitchtools.HarmonicDiatonicInterval('minor', -6).staff_spaces == 5
    assert pitchtools.HarmonicDiatonicInterval('major', -6).staff_spaces == 5
    assert pitchtools.HarmonicDiatonicInterval('minor', -7).staff_spaces == 6
    assert pitchtools.HarmonicDiatonicInterval('major', -7).staff_spaces == 6
    assert pitchtools.HarmonicDiatonicInterval('perfect', -8).staff_spaces == 7
