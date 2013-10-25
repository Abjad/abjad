# -*- encoding: utf-8 -*-
from abjad import *


def test_PhrasingSlurSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    phrasing_slur = spannertools.PhrasingSlurSpanner(direction=Up)
    phrasing_slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 ^ \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_PhrasingSlurSpanner_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    phrasing_slur = spannertools.PhrasingSlurSpanner(direction=Down)
    phrasing_slur.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 _ \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert inspect(staff).is_well_formed()
