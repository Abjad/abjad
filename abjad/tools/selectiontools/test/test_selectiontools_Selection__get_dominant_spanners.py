# -*- coding: utf-8 -*-
import abjad
import pytest


def test_selectiontools_Selection__get_dominant_spanners_01():
    r'''Returns Python list of (spanner, index) pairs.
    Each (spanner, index) pair gives a spanner which dominates
    all components in list, together with the start-index
    at which spanner abjad.attaches to subelement of first
    component in list.
    Beam and trill dominate first container.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    assert format(voice) == abjad.String.normalize(
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

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    receipt = voice[1:2]._get_dominant_spanners()

    assert len(receipt) == 3
    assert (beam, 2) in receipt
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_selectiontools_Selection__get_dominant_spanners_03():
    r'''Glissando and trill dominate last container.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    receipt = voice[-1:]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (glissando, 2) in receipt
    assert (trill, 4) in receipt


def test_selectiontools_Selection__get_dominant_spanners_04():
    r'''Beam and trill dominate first two containers.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    receipt= voice[:2]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_selectiontools_Selection__get_dominant_spanners_05():
    r'''Glissando and trill dominate last two containers.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    receipt = voice[-2:]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_selectiontools_Selection__get_dominant_spanners_06():
    r'''Only trill dominates all three containers.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    receipt = voice[:]._get_dominant_spanners()

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_selectiontools_Selection__get_dominant_spanners_07():
    r'''Only trill dominates voice.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    receipt = abjad.select(voice)._get_dominant_spanners()

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_selectiontools_Selection__get_dominant_spanners_08():
    r'''Only trill dominates first two notes.
    abjad.Note that trill abjad.attaches to notes.
    abjad.Note that beam and glissando abjad.attach to containers.
    '''

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:4])
    glissando = abjad.Glissando()
    abjad.attach(glissando, leaves[-4:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    receipt = abjad.select(leaves[:2])._get_dominant_spanners()

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt
