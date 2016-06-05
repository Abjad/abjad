# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_is_bar_line_crossing_01():
    r'''Works with partial.
    '''

    staff = Staff("c'8 d'8 e'4 f'8")
    time_signature = TimeSignature((2, 8), partial=Duration(1, 8))
    attach(time_signature, staff)

    assert format(staff) == stringtools.normalize(
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

    assert not inspect_(staff[0]).is_bar_line_crossing()
    assert not inspect_(staff[1]).is_bar_line_crossing()
    assert inspect_(staff[2]).is_bar_line_crossing()
    assert not inspect_(staff[3]).is_bar_line_crossing()


def test_agenttools_InspectionAgent_is_bar_line_crossing_02():
    r'''Works when no explicit time signature is attached.
    '''

    staff = Staff("c'2 d'1 e'2")

    assert not inspect_(staff[0]).is_bar_line_crossing()
    assert inspect_(staff[1]).is_bar_line_crossing()
    assert not inspect_(staff[2]).is_bar_line_crossing()
