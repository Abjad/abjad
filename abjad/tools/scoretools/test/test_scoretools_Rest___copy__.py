# -*- coding: utf-8 -*-
from abjad import *
import copy


def test_scoretools_Rest___copy___01():
    r'''Copy rest.
    '''

    rest_1 = Rest((1, 4))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert format(rest_1) == format(rest_2)
    assert rest_1 is not rest_2


def test_scoretools_Rest___copy___02():
    r'''Copy rest with LilyPond multiplier.
    '''

    rest_1 = Rest('r4')
    attach(Multiplier(1, 2), rest_1)
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert format(rest_1) == format(rest_2)
    assert rest_1 is not rest_2


def test_scoretools_Rest___copy___03():
    r'''Copy rest with LilyPond grob overrides and LilyPond context settings.
    '''

    rest_1 = Rest((1, 4))
    override(rest_1).staff.note_head.color = 'red'
    override(rest_1).accidental.color = 'red'
    set_(rest_1).tuplet_full_length = True
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert format(rest_1) == format(rest_2)
    assert rest_1 is not rest_2
