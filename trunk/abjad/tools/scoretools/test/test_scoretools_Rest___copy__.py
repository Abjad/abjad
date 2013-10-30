# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_scoretools_Rest___copy___01():
    r'''Copy rest.
    '''

    rest_1 = Rest((1, 4))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert rest_1.lilypond_format == rest_2.lilypond_format
    assert rest_1 is not rest_2


def test_scoretools_Rest___copy___02():
    r'''Copy rest with LilyPond multiplier.
    '''

    rest_1 = Rest((1, 4), (1, 2))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert rest_1.lilypond_format == rest_2.lilypond_format
    assert rest_1 is not rest_2


def test_scoretools_Rest___copy___03():
    r'''Copy rest with LilyPond grob overrides and LilyPond context settings.
    '''

    rest_1 = Rest((1, 4))
    rest_1.override.staff.note_head.color = 'red'
    rest_1.override.accidental.color = 'red'
    rest_1.set.tuplet_full_length = True
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert rest_1.lilypond_format == rest_2.lilypond_format
    assert rest_1 is not rest_2
