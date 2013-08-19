# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval___sub___01():

    major_second_ascending = pitchtools.NamedMelodicInterval('major', 2)
    major_third_ascending = pitchtools.NamedMelodicInterval('major', 3)

    difference = major_second_ascending - major_third_ascending
    assert difference == pitchtools.NamedMelodicInterval('major', -2)

    difference = major_third_ascending - major_second_ascending
    assert difference == pitchtools.NamedMelodicInterval('major', 2)

    difference = major_second_ascending - major_second_ascending
    assert difference == pitchtools.NamedMelodicInterval('perfect', 1)

    difference = major_third_ascending - major_third_ascending
    assert difference == pitchtools.NamedMelodicInterval('perfect', 1)
