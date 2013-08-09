# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_split_leaves_in_expr_in_halves_01():
    r'''Meiose each leaf in two.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    leaftools.split_leaves_in_expr_in_halves(voice)

    r'''
    \new Voice {
      c'16 [
      c'16
      d'16
      d'16
      e'16
      e'16 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'16 [
            c'16
            d'16
            d'16
            e'16
            e'16 ]
        }
        '''
        )


def test_leaftools_split_leaves_in_expr_in_halves_02():
    r'''Meiose one leaf in four.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    leaftools.split_leaves_in_expr_in_halves(voice[0], 4)

    r'''
    \new Voice {
      c'32 [
      c'32
      c'32
      c'32
      d'8
      e'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'32 [
            c'32
            c'32
            c'32
            d'8
            e'8 ]
        }
        '''
        )
