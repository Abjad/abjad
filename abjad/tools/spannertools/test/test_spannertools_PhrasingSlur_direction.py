# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_PhrasingSlur_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.PhrasingSlur(direction=Up)
    attach(slur, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 ^ \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_PhrasingSlur_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.PhrasingSlur(direction=Down)
    attach(slur, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 _ \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert inspect_(staff).is_well_formed()