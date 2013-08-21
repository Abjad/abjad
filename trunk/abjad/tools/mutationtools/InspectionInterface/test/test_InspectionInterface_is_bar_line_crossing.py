# -*- encoding: utf-8 -*-
from abjad import *


def test_InspectionInterface_is_bar_line_crossing_01():
    r'''Works with partial.
    '''

    staff = Staff("c'8 d'8 e'4 f'8")
    time_signature = contexttools.TimeSignatureMark(
        (2, 8), partial=Duration(1, 8))
    time_signature.attach(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \partial 8
            \time 2/8
            c'8
            d'8
            e'4
            f'8
        }
        '''
        )

    assert not inspect(staff[0]).is_bar_line_crossing()
    assert not inspect(staff[1]).is_bar_line_crossing()
    assert inspect(staff[2]).is_bar_line_crossing()
    assert not inspect(staff[3]).is_bar_line_crossing()


def test_InspectionInterface_is_bar_line_crossing_02():
    r'''Works when no explicit time signature is attached.
    '''

    staff = Staff("c'2 d'1 e'2")

    assert not inspect(staff[0]).is_bar_line_crossing()
    assert inspect(staff[1]).is_bar_line_crossing()
    assert not inspect(staff[2]).is_bar_line_crossing()
