# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Leaf_get_duration_01():
    r'''Clock duration equals prolated duration divide by effective tempo.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 4), 38)(staff)
    contexttools.TempoMark(Duration(1, 4), 42)(staff[2])
    Score([staff])

    r'''
    \new Staff {
        \tempo 4=38
        c'8
        d'8
        \tempo 4=42
        e'8
        f'8
    }
    '''

    assert staff[0].get_duration(in_seconds=True) == Duration(15, 19)
    assert staff[1].get_duration(in_seconds=True) == Duration(15, 19)
    assert staff[2].get_duration(in_seconds=True) == Duration(5, 7)
    assert staff[3].get_duration(in_seconds=True) == Duration(5, 7)


def test_Leaf_get_duration_02():
    r'''Clock duration can not calculate without tempo.
    '''

    t = Note("c'4")
    assert py.test.raises(MissingTempoError, 't.get_duration(in_seconds=True)')
