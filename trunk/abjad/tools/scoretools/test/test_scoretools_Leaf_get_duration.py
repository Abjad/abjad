# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_leaftools_Leaf_get_duration_01():
    r'''Clock duration equals prolated duration divide by effective tempo.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = contexttools.TempoMark(Duration(1, 4), 38)
    attach(tempo, staff)
    tempo = contexttools.TempoMark(Duration(1, 4), 42)
    attach(tempo, staff[2])
    Score([staff])

    assert testtools.compare(
        staff,
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
        )

    assert inspect(staff[0]).get_duration(in_seconds=True) == Duration(15, 19)
    assert inspect(staff[1]).get_duration(in_seconds=True) == Duration(15, 19)
    assert inspect(staff[2]).get_duration(in_seconds=True) == Duration(5, 7)
    assert inspect(staff[3]).get_duration(in_seconds=True) == Duration(5, 7)


def test_leaftools_Leaf_get_duration_02():
    r'''Clock duration can not calculate without tempo.
    '''

    note = Note("c'4")
    statement = 'inspect(note).get_duration(in_seconds=True)'
    assert py.test.raises(MissingTempoError, statement)
