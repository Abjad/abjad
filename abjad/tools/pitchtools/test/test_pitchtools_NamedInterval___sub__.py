# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval___sub___01():

    major_second_ascending = pitchtools.NamedInterval('major', 2)
    major_third_ascending = pitchtools.NamedInterval('major', 3)

    difference = major_second_ascending - major_third_ascending
    assert difference == pitchtools.NamedInterval('major', -2)

    difference = major_third_ascending - major_second_ascending
    assert difference == pitchtools.NamedInterval('major', 2)

    difference = major_second_ascending - major_second_ascending
    assert difference == pitchtools.NamedInterval('perfect', 1)

    difference = major_third_ascending - major_third_ascending
    assert difference == pitchtools.NamedInterval('perfect', 1)
