# -*- encoding: utf-8 -*-
from abjad import *


def test_PhrasingSlurSpanner___init___01():
    r'''Init empty phrasing slur.
    '''

    phrasing_slur = spannertools.PhrasingSlurSpanner()
    assert isinstance(phrasing_slur, spannertools.PhrasingSlurSpanner)


def test_PhrasingSlurSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8")
    phrasing_slur = spannertools.PhrasingSlurSpanner()
    phrasing_slur.attach(staff.select_leaves())

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
