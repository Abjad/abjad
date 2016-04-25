# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_rests_01():
    r'''Make rest.
    '''

    rest = scoretools.make_rests((1, 4))
    assert isinstance(rest, selectiontools.Selection)
    assert len(rest) == 1
    assert isinstance(rest[0], Rest)
    assert rest[0].written_duration == Duration(1, 4)
    assert len(inspect_(rest[0]).get_logical_tie()) == 1


def test_scoretools_make_rests_02():
    r'''Do not tie rests.
    '''

    rest = scoretools.make_rests((5, 8))
    assert len(rest) == 2
    assert isinstance(rest[0], Rest)
    assert isinstance(rest[1], Rest)
    assert rest[0].written_duration == Duration(4, 8)
    assert rest[1].written_duration == Duration(1, 8)
    assert all(len(inspect_(x).get_logical_tie()) == 1 for x in rest)


def test_scoretools_make_rests_03():
    r'''Do not tie rests.
    '''

    true = scoretools.make_rests((5, 8), tie_parts=True)
    assert all(len(inspect_(x).get_logical_tie()) == 1 for x in true)


def test_scoretools_make_rests_04():
    r'''Make rests.
    '''

    t = scoretools.make_rests([(1, 4), Duration(1, 8)])
    assert t[0].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)
    assert all(len(inspect_(x).get_logical_tie()) == 1 for x in t)
