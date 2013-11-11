# -*- encoding: utf-8 -*-
from experimental import *


def test_ReiteratedDynamicHandler___call___01():

    handler = handlertools.ReiteratedDynamicHandler('f')
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    handler(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \f
            d'8 \f
            r8
            e'8 \f
            f'8 \f
            r8
            g'8 \f
            r8
            a'32 \f
            b'32 \f
            r8.
            c''8 \f
            d''8 \f
        }
        '''
        )
