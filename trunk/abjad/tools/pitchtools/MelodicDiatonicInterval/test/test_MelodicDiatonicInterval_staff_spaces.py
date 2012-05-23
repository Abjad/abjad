from abjad import *


def test_MelodicDiatonicInterval_staff_spaces_01():

    assert pitchtools.MelodicDiatonicInterval('perfect', 1).staff_spaces == 0
    assert pitchtools.MelodicDiatonicInterval('minor', 2).staff_spaces == 1
    assert pitchtools.MelodicDiatonicInterval('major', 2).staff_spaces == 1
    assert pitchtools.MelodicDiatonicInterval('minor', 3).staff_spaces == 2
    assert pitchtools.MelodicDiatonicInterval('major', 3).staff_spaces == 2
    assert pitchtools.MelodicDiatonicInterval('perfect', 4).staff_spaces == 3
    assert pitchtools.MelodicDiatonicInterval('augmented', 4).staff_spaces == 3
    assert pitchtools.MelodicDiatonicInterval('diminished', 5).staff_spaces == 4
    assert pitchtools.MelodicDiatonicInterval('perfect', 5).staff_spaces == 4
    assert pitchtools.MelodicDiatonicInterval('minor', 6).staff_spaces == 5
    assert pitchtools.MelodicDiatonicInterval('major', 6).staff_spaces == 5
    assert pitchtools.MelodicDiatonicInterval('minor', 7).staff_spaces == 6
    assert pitchtools.MelodicDiatonicInterval('major', 7).staff_spaces == 6
    assert pitchtools.MelodicDiatonicInterval('perfect', 8).staff_spaces == 7


def test_MelodicDiatonicInterval_staff_spaces_02():

    assert pitchtools.MelodicDiatonicInterval('perfect', -1).staff_spaces == 0
    assert pitchtools.MelodicDiatonicInterval('minor', -2).staff_spaces == -1
    assert pitchtools.MelodicDiatonicInterval('major', -2).staff_spaces == -1
    assert pitchtools.MelodicDiatonicInterval('minor', -3).staff_spaces == -2
    assert pitchtools.MelodicDiatonicInterval('major', -3).staff_spaces == -2
    assert pitchtools.MelodicDiatonicInterval('perfect', -4).staff_spaces == -3
    assert pitchtools.MelodicDiatonicInterval('augmented', -4).staff_spaces == -3
    assert pitchtools.MelodicDiatonicInterval('diminished', -5).staff_spaces == -4
    assert pitchtools.MelodicDiatonicInterval('perfect', -5).staff_spaces == -4
    assert pitchtools.MelodicDiatonicInterval('minor', -6).staff_spaces == -5
    assert pitchtools.MelodicDiatonicInterval('major', -6).staff_spaces == -5
    assert pitchtools.MelodicDiatonicInterval('minor', -7).staff_spaces == -6
    assert pitchtools.MelodicDiatonicInterval('major', -7).staff_spaces == -6
    assert pitchtools.MelodicDiatonicInterval('perfect', -8).staff_spaces == -7
