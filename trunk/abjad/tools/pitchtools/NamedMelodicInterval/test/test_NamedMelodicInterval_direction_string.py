# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval_direction_string_01():

    assert pitchtools.NamedMelodicInterval('perfect', 1).direction_string is \
        None
    assert pitchtools.NamedMelodicInterval('minor', 2).direction_string == \
        'ascending'
    assert pitchtools.NamedMelodicInterval('major', 2).direction_string == \
        'ascending'
    assert pitchtools.NamedMelodicInterval('minor', 3).direction_string == \
        'ascending'
    assert pitchtools.NamedMelodicInterval('major', 3).direction_string == \
        'ascending'


def test_NamedMelodicInterval_direction_string_02():

    assert pitchtools.NamedMelodicInterval('perfect', -1).direction_string \
        is None
    assert pitchtools.NamedMelodicInterval('minor', -2).direction_string == \
        'descending'
    assert pitchtools.NamedMelodicInterval('major', -2).direction_string == \
        'descending'
    assert pitchtools.NamedMelodicInterval('minor', -3).direction_string == \
        'descending'
    assert pitchtools.NamedMelodicInterval('major', -3).direction_string == \
        'descending'
