# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_split_leaf_in_halves_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.select_leaves())

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    leaftools.split_leaf_in_halves(staff[0], n=4)


    r'''
    \new Staff {
        c'32 [
        c'32
        c'32
        c'32
        d'8
        e'8
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'32 [
            c'32
            c'32
            c'32
            d'8
            e'8
            f'8 ]
        }
        '''
        )
