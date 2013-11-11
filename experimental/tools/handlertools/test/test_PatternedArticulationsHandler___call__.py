# -*- encoding: utf-8 -*-
from experimental import *


def test_PatternedArticulationsHandler___call___01():

    handler = handlertools.PatternedArticulationsHandler([['>', '-'], ['.']])
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8")
    handler(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 -\accent -\tenuto
            d'8 -\staccato
            r8
            e'8 -\accent -\tenuto
            f'8 -\staccato
            r8
            g'8 -\accent -\tenuto
            r8
        }
        '''
        )
