# -*- encoding: utf-8 -*-
from experimental import *


def test_ReiteratedArticulationHandler___call___01():

    handler = handlertools.ReiteratedArticulationHandler(['^', '.'])
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8")
    handler(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 -\marcato -\staccato
            d'8 -\marcato -\staccato
            r8
            e'8 -\marcato -\staccato
            f'8 -\marcato -\staccato
            r8
            g'8 -\marcato -\staccato
            r8
        }
        '''
        )


def test_ReiteratedArticulationHandler___call___02():

    handler = handlertools.ReiteratedArticulationHandler('.')
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8")
    handler(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 -\staccato
            d'8 -\staccato
            r8
            e'8 -\staccato
            f'8 -\staccato
            r8
            g'8 -\staccato
            r8
        }
        '''
        )
