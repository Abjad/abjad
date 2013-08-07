# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_repeat_leaves_in_expr_01():
    r'''Multiply each leaf in voice by 1.
    '''

    voice = Voice("c'8 d'8 e'8")
    p = spannertools.BeamSpanner(voice[:])
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

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
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

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    leaftools.repeat_leaves_in_expr(t, total=3)

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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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
