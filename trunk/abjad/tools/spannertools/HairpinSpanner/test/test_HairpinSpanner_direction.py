# -*- encoding: utf-8 -*-
from abjad import *


def test_HairpinSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = spannertools.HairpinSpanner(descriptor='p < f', direction=Down)
    hairpin.attach(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 _ \< _ \p
            d'8
            e'8
            f'8 _ \f
        }
        '''
        )
