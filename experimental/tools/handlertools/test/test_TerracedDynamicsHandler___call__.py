# -*- encoding: utf-8 -*-
from experimental import *


def test_TerracedDynamicsHandler___call___01():

    handler = handlertools.TerracedDynamicsHandler(['f', 'mp', 'mf', 'mp', 'ff'])
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    handler(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \f
            d'8 \mp
            r8
            e'8 \mf
            f'8 \mp
            r8
            g'8 \ff
            r8
            a'32 \f
            b'32 \mp
            r8.
            c''8 \mf
            d''8 \mp
        }
        '''
        )
