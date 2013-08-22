# -*- encoding: utf-8 -*-
from abjad import *


def test_DynamicTextSpanner_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    spannertools.DynamicTextSpanner(voice[:2], 'f')
    spannertools.DynamicTextSpanner(voice[2:], 'p')

    r'''
    \new Voice {
        c'8 [ \f
        d'8
        e'8 \p
        f'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \f
            d'8
            e'8 \p
            f'8 ]
        }
        '''
        )
    #assert voice[0].dynamics.effective == 'f'
    #assert voice[1].dynamics.effective == 'f'
    #assert voice[2].dynamics.effective == 'p'
    #assert voice[3].dynamics.effective == 'p'
