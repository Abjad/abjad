# -*- encoding: utf-8 -*-
from experimental import *


def test_TerracedDynamicsHandler_new_01():

    handler = handlertools.TerracedDynamicsHandler()
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    new(handler, ['p', 'f'])(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \p
            d'8 \f
            r8
            e'8 \p
            f'8 \f
            r8
            g'8 \p
            r8
            a'32 \f
            b'32 \p
            r8.
            c''8 \f
            d''8 \p
        }
        '''
        )
