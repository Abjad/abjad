# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_repeat_leaves_in_expr_01():
    r'''Multiply each leaf in voice by 1.
    '''

    voice = Voice("c'8 d'8 e'8")
    beam = spannertools.BeamSpanner(voice[:])
    leaftools.repeat_leaves_in_expr(voice, total=2)

    r'''
    \new Voice {
      c'8 [
      c'8
      d'8
      d'8
      e'8
      e'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            c'8
            d'8
            d'8
            e'8
            e'8 ]
        }
        '''
        )


def test_leaftools_repeat_leaves_in_expr_02():
    r'''Multiply each leaf in voice by 2.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    leaftools.repeat_leaves_in_expr(voice, total=3)

    r'''
    \new Voice {
      c'8 [
      c'8
      c'8
      d'8
      d'8
      d'8
      e'8
      e'8
      e'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            c'8
            c'8
            d'8
            d'8
            d'8
            e'8
            e'8
            e'8 ]
        }
        '''
        )
