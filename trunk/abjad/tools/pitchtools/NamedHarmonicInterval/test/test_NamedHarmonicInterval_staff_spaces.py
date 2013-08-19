# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval_staff_spaces_01():

    assert pitchtools.NamedHarmonicInterval('perfect', 1).staff_spaces == 0
    assert pitchtools.NamedHarmonicInterval('minor', 2).staff_spaces == 1
    assert pitchtools.NamedHarmonicInterval('major', 2).staff_spaces == 1
    assert pitchtools.NamedHarmonicInterval('minor', 3).staff_spaces == 2
    assert pitchtools.NamedHarmonicInterval('major', 3).staff_spaces == 2
    assert pitchtools.NamedHarmonicInterval('perfect', 4).staff_spaces == 3
    assert pitchtools.NamedHarmonicInterval('augmented', 4).staff_spaces == 3
    assert pitchtools.NamedHarmonicInterval('diminished', 5).staff_spaces == 4
    assert pitchtools.NamedHarmonicInterval('perfect', 5).staff_spaces == 4
    assert pitchtools.NamedHarmonicInterval('minor', 6).staff_spaces == 5
    assert pitchtools.NamedHarmonicInterval('major', 6).staff_spaces == 5
    assert pitchtools.NamedHarmonicInterval('minor', 7).staff_spaces == 6
    assert pitchtools.NamedHarmonicInterval('major', 7).staff_spaces == 6
    assert pitchtools.NamedHarmonicInterval('perfect', 8).staff_spaces == 7


def test_NamedHarmonicInterval_staff_spaces_02():

    assert pitchtools.NamedHarmonicInterval('perfect', -1).staff_spaces == 0
    assert pitchtools.NamedHarmonicInterval('minor', -2).staff_spaces == 1
    assert pitchtools.NamedHarmonicInterval('major', -2).staff_spaces == 1
    assert pitchtools.NamedHarmonicInterval('minor', -3).staff_spaces == 2
    assert pitchtools.NamedHarmonicInterval('major', -3).staff_spaces == 2
    assert pitchtools.NamedHarmonicInterval('perfect', -4).staff_spaces == 3
    assert pitchtools.NamedHarmonicInterval('augmented', -4).staff_spaces == 3
    assert pitchtools.NamedHarmonicInterval('diminished', -5).staff_spaces == 4
    assert pitchtools.NamedHarmonicInterval('perfect', -5).staff_spaces == 4
    assert pitchtools.NamedHarmonicInterval('minor', -6).staff_spaces == 5
    assert pitchtools.NamedHarmonicInterval('major', -6).staff_spaces == 5
    assert pitchtools.NamedHarmonicInterval('minor', -7).staff_spaces == 6
    assert pitchtools.NamedHarmonicInterval('major', -7).staff_spaces == 6
    assert pitchtools.NamedHarmonicInterval('perfect', -8).staff_spaces == 7
