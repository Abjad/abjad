# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_divide_leaves_in_expr_meiotically_01():
    r'''Meiose each leaf in two.
    '''

    voice = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(voice[:])
    leaftools.divide_leaves_in_expr_meiotically(voice)

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
        voice.lilypond_format,
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


def test_leaftools_divide_leaves_in_expr_meiotically_02():
    r'''Meiose one leaf in four.
    '''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    leaftools.divide_leaves_in_expr_meiotically(t[0], 4)

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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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
