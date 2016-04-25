# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval_direction_string_01():

    assert pitchtools.NamedInterval('perfect', 1).direction_string is \
        None
    assert pitchtools.NamedInterval('minor', 2).direction_string == \
        'ascending'
    assert pitchtools.NamedInterval('major', 2).direction_string == \
        'ascending'
    assert pitchtools.NamedInterval('minor', 3).direction_string == \
        'ascending'
    assert pitchtools.NamedInterval('major', 3).direction_string == \
        'ascending'


def test_pitchtools_NamedInterval_direction_string_02():

    assert pitchtools.NamedInterval('perfect', -1).direction_string \
        is None
    assert pitchtools.NamedInterval('minor', -2).direction_string == \
        'descending'
    assert pitchtools.NamedInterval('major', -2).direction_string == \
        'descending'
    assert pitchtools.NamedInterval('minor', -3).direction_string == \
        'descending'
    assert pitchtools.NamedInterval('major', -3).direction_string == \
        'descending'
