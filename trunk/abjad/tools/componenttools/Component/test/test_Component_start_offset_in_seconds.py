# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Component_start_offset_in_seconds_01():
    r'''Offset seconds can not calculate without excplit tempo indication.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    statement = 'more(staff[0]).get_timespan(in_seconds=True).start_offset'
    assert py.test.raises(MissingTempoError, statement)


def test_Component_start_offset_in_seconds_02():
    r'''Offset seconds work with explicit tempo indication.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 8), 48, target_context=Staff)(staff)

    r'''
    \new Staff {
        \tempo 8=48
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert more(staff[0]).get_timespan(in_seconds=True).start_offset == Duration(0)
    assert more(staff[1]).get_timespan(in_seconds=True).start_offset == Duration(5, 4)
