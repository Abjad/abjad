# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval_staff_spaces_01():

    assert pitchtools.NamedMelodicInterval('perfect', 1).staff_spaces == 0
    assert pitchtools.NamedMelodicInterval('minor', 2).staff_spaces == 1
    assert pitchtools.NamedMelodicInterval('major', 2).staff_spaces == 1
    assert pitchtools.NamedMelodicInterval('minor', 3).staff_spaces == 2
    assert pitchtools.NamedMelodicInterval('major', 3).staff_spaces == 2
    assert pitchtools.NamedMelodicInterval('perfect', 4).staff_spaces == 3
    assert pitchtools.NamedMelodicInterval('augmented', 4).staff_spaces == 3
    assert pitchtools.NamedMelodicInterval('diminished', 5).staff_spaces == 4
    assert pitchtools.NamedMelodicInterval('perfect', 5).staff_spaces == 4
    assert pitchtools.NamedMelodicInterval('minor', 6).staff_spaces == 5
    assert pitchtools.NamedMelodicInterval('major', 6).staff_spaces == 5
    assert pitchtools.NamedMelodicInterval('minor', 7).staff_spaces == 6
    assert pitchtools.NamedMelodicInterval('major', 7).staff_spaces == 6
    assert pitchtools.NamedMelodicInterval('perfect', 8).staff_spaces == 7


def test_NamedMelodicInterval_staff_spaces_02():

    assert pitchtools.NamedMelodicInterval('perfect', -1).staff_spaces == 0
    assert pitchtools.NamedMelodicInterval('minor', -2).staff_spaces == -1
    assert pitchtools.NamedMelodicInterval('major', -2).staff_spaces == -1
    assert pitchtools.NamedMelodicInterval('minor', -3).staff_spaces == -2
    assert pitchtools.NamedMelodicInterval('major', -3).staff_spaces == -2
    assert pitchtools.NamedMelodicInterval('perfect', -4).staff_spaces == -3
    assert pitchtools.NamedMelodicInterval('augmented', -4).staff_spaces == -3
    assert pitchtools.NamedMelodicInterval('diminished', -5).staff_spaces == -4
    assert pitchtools.NamedMelodicInterval('perfect', -5).staff_spaces == -4
    assert pitchtools.NamedMelodicInterval('minor', -6).staff_spaces == -5
    assert pitchtools.NamedMelodicInterval('major', -6).staff_spaces == -5
    assert pitchtools.NamedMelodicInterval('minor', -7).staff_spaces == -6
    assert pitchtools.NamedMelodicInterval('major', -7).staff_spaces == -6
    assert pitchtools.NamedMelodicInterval('perfect', -8).staff_spaces == -7
