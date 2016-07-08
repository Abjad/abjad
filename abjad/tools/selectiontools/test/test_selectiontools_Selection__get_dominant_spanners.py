# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_selectiontools_Selection__get_dominant_spanners_01():
    r'''Returns Python list of (spanner, index) pairs.
    Each (spanner, index) pair gives a spanner which dominates
    all components in list, together with the start-index
    at which spanner attaches to subelement of first
    component in list.
    Beam and trill dominate first container.
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

    receipt = voice[:1]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_selectiontools_Selection__get_dominant_spanners_02():
    r'''Beam, glissando and trill all dominate second container.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    receipt = voice[1:2]._get_dominant_spanners()

    assert len(receipt) == 3
    assert (beam, 2) in receipt
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_selectiontools_Selection__get_dominant_spanners_03():
    r'''Glissando and trill dominate last container.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    receipt = voice[-1:]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (glissando, 2) in receipt
    assert (trill, 4) in receipt


def test_selectiontools_Selection__get_dominant_spanners_04():
    r'''Beam and trill dominate first two containers.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    receipt= voice[:2]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_selectiontools_Selection__get_dominant_spanners_05():
    r'''Glissando and trill dominate last two containers.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    receipt = voice[-2:]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_selectiontools_Selection__get_dominant_spanners_06():
    r'''Only trill dominates all three containers.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    receipt = voice[:]._get_dominant_spanners()

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_selectiontools_Selection__get_dominant_spanners_07():
    r'''Only trill dominates voice.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    receipt = select(voice)._get_dominant_spanners()

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_selectiontools_Selection__get_dominant_spanners_08():
    r'''Only trill dominates first two notes.
    Note that trill attaches to notes.
    Note that beam and glissando attach to containers.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves[:4])
    glissando = spannertools.Glissando()
    attach(glissando, leaves[-4:])
    trill = spannertools.TrillSpanner()
    attach(trill, leaves)

    receipt = select(leaves[:2])._get_dominant_spanners()

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt
