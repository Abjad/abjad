# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DecrescendoSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    decrescendo = DecrescendoSpanner(direction=Up)
    attach(decrescendo, staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 ^ \>
            d'8
            e'8
            f'8 \!
            g'2
        }
        '''
        )
