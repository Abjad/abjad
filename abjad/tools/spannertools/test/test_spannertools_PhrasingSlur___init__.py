# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_PhrasingSlur___init___01():
    r'''Initialize empty phrasing slur.
    '''

    phrasing_slur = spannertools.PhrasingSlur()
    assert isinstance(phrasing_slur, spannertools.PhrasingSlur)


def test_spannertools_PhrasingSlur___init___02():

    staff = Staff("c'8 d'8 e'8 f'8")
    phrasing_slur = spannertools.PhrasingSlur()
    attach(phrasing_slur, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert inspect_(staff).is_well_formed()