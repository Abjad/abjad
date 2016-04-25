# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval_staff_spaces_01():

    assert pitchtools.NamedInterval('perfect', 1).staff_spaces == 0
    assert pitchtools.NamedInterval('minor', 2).staff_spaces == 1
    assert pitchtools.NamedInterval('major', 2).staff_spaces == 1
    assert pitchtools.NamedInterval('minor', 3).staff_spaces == 2
    assert pitchtools.NamedInterval('major', 3).staff_spaces == 2
    assert pitchtools.NamedInterval('perfect', 4).staff_spaces == 3
    assert pitchtools.NamedInterval('augmented', 4).staff_spaces == 3
    assert pitchtools.NamedInterval('diminished', 5).staff_spaces == 4
    assert pitchtools.NamedInterval('perfect', 5).staff_spaces == 4
    assert pitchtools.NamedInterval('minor', 6).staff_spaces == 5
    assert pitchtools.NamedInterval('major', 6).staff_spaces == 5
    assert pitchtools.NamedInterval('minor', 7).staff_spaces == 6
    assert pitchtools.NamedInterval('major', 7).staff_spaces == 6
    assert pitchtools.NamedInterval('perfect', 8).staff_spaces == 7


def test_pitchtools_NamedInterval_staff_spaces_02():

    assert pitchtools.NamedInterval('perfect', -1).staff_spaces == 0
    assert pitchtools.NamedInterval('minor', -2).staff_spaces == -1
    assert pitchtools.NamedInterval('major', -2).staff_spaces == -1
    assert pitchtools.NamedInterval('minor', -3).staff_spaces == -2
    assert pitchtools.NamedInterval('major', -3).staff_spaces == -2
    assert pitchtools.NamedInterval('perfect', -4).staff_spaces == -3
    assert pitchtools.NamedInterval('augmented', -4).staff_spaces == -3
    assert pitchtools.NamedInterval('diminished', -5).staff_spaces == -4
    assert pitchtools.NamedInterval('perfect', -5).staff_spaces == -4
    assert pitchtools.NamedInterval('minor', -6).staff_spaces == -5
    assert pitchtools.NamedInterval('major', -6).staff_spaces == -5
    assert pitchtools.NamedInterval('minor', -7).staff_spaces == -6
    assert pitchtools.NamedInterval('major', -7).staff_spaces == -6
    assert pitchtools.NamedInterval('perfect', -8).staff_spaces == -7
