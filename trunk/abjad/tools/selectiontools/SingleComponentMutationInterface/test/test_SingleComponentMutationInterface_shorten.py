# -*- encoding: utf-8 -*-
from abjad import *


def test_SingleComponentMutationInterface_shorten_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    mutate(voice).shorten(Duration(1, 8) + Duration(1, 20))

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 4/5 {
                d'16. [
            }
            e'8
            f'8 ]
        }
        '''
        )


def test_SingleComponentMutationInterface_shorten_02():

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    mutate(voice).shorten(Duration(3, 16))

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            d'16 [
            e'8
            f'8 ]
        }
        '''
        )
