# -*- encoding: utf-8 -*-
from abjad import *


def test_DuratedComplexBeamSpanner_lone_01():
    r'''Span lone note when lone is set to true.
    '''

    voice = Voice("c'8")
    spannertools.DuratedComplexBeamSpanner(voice, lone=True)

    r'''
    \new Voice {
        \set stemLeftBeamCount = #1
        \set stemRightBeamCount = #1
        c'8 [ ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            c'8 [ ]
        }
        '''
        )


def test_DuratedComplexBeamSpanner_lone_02():
    r'''Do not span lone note when lone is set to false.
    '''

    t = Voice("c'8")
    spannertools.DuratedComplexBeamSpanner(t, lone=False)

    r'''
    \new Voice {
        c'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8
        }
        '''
        )


def test_DuratedComplexBeamSpanner_lone_03():
    r'''Ignore lone when spanner spans more than one leaf.
    '''

    t = Voice("c'8 d'8")
    spannertools.DuratedComplexBeamSpanner(t, lone=False)

    r'''
    \new Voice {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #1
        c'8 [
        \set stemLeftBeamCount = #1
        \set stemRightBeamCount = #0
        d'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #1
            c'8 [
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #0
            d'8 ]
        }
        '''
        )
