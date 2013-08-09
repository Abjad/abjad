# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_withdraw_components_from_spanners_covered_by_components_01():
    r'''Withdraw from all spanners covered by components.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:2])
    spannertools.SlurSpanner(voice[:])

    r'''
    \new Voice {
        c'8 [ (
        d'8 ]
        e'8
        f'8 )
    }
    '''

    spannertools.withdraw_components_from_spanners_covered_by_components(voice[:2])

    r'''
    \new Voice {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )
