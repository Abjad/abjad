# -*- encoding: utf-8 -*-
from abjad import *


def test_CrescendoSpanner___init___01():
    r'''Init empty crescendo spanner.
    '''

    crescendo = spannertools.CrescendoSpanner()
    assert isinstance(crescendo, spannertools.CrescendoSpanner)


def test_CrescendoSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \<
            d'8
            e'8
            f'8 \!
            g'2
        }
        '''
        )
