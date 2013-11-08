# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_PhrasingSlur___init___01():
    r'''Init empty phrasing slur.
    '''

    phrasing_slur = spannertools.PhrasingSlur()
    assert isinstance(phrasing_slur, spannertools.PhrasingSlur)


def test_spannertools_PhrasingSlur___init___02():

    staff = Staff("c'8 d'8 e'8 f'8")
    phrasing_slur = spannertools.PhrasingSlur()
    attach(phrasing_slur, staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \(
            d'8
            e'8
            f'8 \)
        }
        '''
        )

    assert inspect(staff).is_well_formed()
