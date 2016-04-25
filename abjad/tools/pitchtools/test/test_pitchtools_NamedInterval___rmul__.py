# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___rmul___01():

    major_second = pitchtools.NamedInterval('major', 2)

    assert 0 * major_second == pitchtools.NamedInterval('perfect', 1)
    assert 1 * major_second == pitchtools.NamedInterval('major', 2)
    assert 2 * major_second == pitchtools.NamedInterval('major', 3)
    assert 3 * major_second == pitchtools.NamedInterval('augmented', 4)
