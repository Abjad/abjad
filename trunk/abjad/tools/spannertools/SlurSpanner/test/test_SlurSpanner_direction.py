# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner_direction_01():
    t = Voice("c'8 d'8 e'8 f'8")
    s = spannertools.SlurSpanner(t, direction=Up)

    r'''
    \new Voice {
        c'8 ^ (
        d'8
        e'8
        f'8 )
    }
    '''

    assert t.get_spanners() == set([s])
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 ^ (
            d'8
            e'8
            f'8 )
        }
        '''
        )
