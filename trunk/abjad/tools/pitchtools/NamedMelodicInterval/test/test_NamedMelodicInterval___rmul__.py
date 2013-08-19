# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___rmul___01():

    major_second = pitchtools.NamedMelodicInterval('major', 2)

    assert 0 * major_second == pitchtools.NamedMelodicInterval('perfect', 1)
    assert 1 * major_second == pitchtools.NamedMelodicInterval('major', 2)
    assert 2 * major_second == pitchtools.NamedMelodicInterval('major', 3)
    assert 3 * major_second == pitchtools.NamedMelodicInterval('augmented', 4)
