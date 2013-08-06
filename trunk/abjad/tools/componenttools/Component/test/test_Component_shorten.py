# -*- encoding: utf-8 -*-
from abjad import *


def test_Component_shorten_01():

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.shorten(Duration(1, 8) + Duration(1, 20))


    r'''
    \new Voice {
        \times 4/5 {
            d'16. [
        }
        e'8
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
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


def test_Component_shorten_02():

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.shorten(Duration(3, 16))

    r'''
    \new Voice {
        d'16 [
        e'8
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            d'16 [
            e'8
            f'8 ]
        }
        '''
        )
