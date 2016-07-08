# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Container__get_spanners_that_dominate_component_pair_01():
    r'''Returns Python list of (spanner, index) pairs.
    Each spanner dominates an empty slice between components.
    No spanners dominate voice[0:0].
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8
            }
            {
                e'8 \glissando
                f'8 ] \glissando
            }
            {
                g'8 \glissando
                a'8 \stopTrillSpan
            }
        }
        '''
        )

    receipt = voice._get_spanners_that_dominate_component_pair(None, voice[0])

    assert len(receipt) == 0
    assert receipt == set([])


def test_scoretools_Container__get_spanners_that_dominate_component_pair_02():
    r'''Beam and trill both dominate crack at voice[1:1].
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8
            }
            {
                e'8 \glissando
                f'8 ] \glissando
            }
            {
                g'8 \glissando
                a'8 \stopTrillSpan
            }
        }
        '''
        )

    pair = (voice[0], voice[1])
    receipt = voice._get_spanners_that_dominate_component_pair(*pair)

    assert len(receipt) == 2
    assert (beam, 2) in receipt
    assert (trill, 2) in receipt


def test_scoretools_Container__get_spanners_that_dominate_component_pair_03():
    r'''Glissando and trill both dominate crack at voice[2:2].
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8
            }
            {
                e'8 \glissando
                f'8 ] \glissando
            }
            {
                g'8 \glissando
                a'8 \stopTrillSpan
            }
        }
        '''
        )

    pair = (voice[1], voice[2])
    receipt = voice._get_spanners_that_dominate_component_pair(*pair)

    assert len(receipt) == 2
    assert (glissando, 2) in receipt
    assert (trill, 4) in receipt


def test_scoretools_Container__get_spanners_that_dominate_component_pair_04():
    r'''No spanners dominate empty slice following voice.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \startTrillSpan
                d'8
            }
            {
                e'8 \glissando
                f'8 ] \glissando
            }
            {
                g'8 \glissando
                a'8 \stopTrillSpan
            }
        }
        '''
        )

    pair = (voice[2], None)
    receipt = voice._get_spanners_that_dominate_component_pair(*pair)

    assert len(receipt) == 0
    assert receipt == set([])
