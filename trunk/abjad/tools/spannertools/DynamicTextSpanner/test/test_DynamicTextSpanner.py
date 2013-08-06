# -*- encoding: utf-8 -*-
from abjad import *


def test_DynamicTextSpanner_01():

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    spannertools.DynamicTextSpanner(t[:2], 'f')
    spannertools.DynamicTextSpanner(t[2:], 'p')

    r'''
    \new Voice {
        c'8 [ \f
        d'8
        e'8 \p
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 [ \f
            d'8
            e'8 \p
            f'8 ]
        }
        '''
        )
    #assert t[0].dynamics.effective == 'f'
    #assert t[1].dynamics.effective == 'f'
    #assert t[2].dynamics.effective == 'p'
    #assert t[3].dynamics.effective == 'p'
