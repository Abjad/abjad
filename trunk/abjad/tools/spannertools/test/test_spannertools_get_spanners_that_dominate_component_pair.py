# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_get_spanners_that_dominate_component_pair_01():
    r'''Return Python list of (spanner, index) pairs.
        Each spanner dominates a *crack* between components.'''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

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

    "No spanners dominate voice[0:0]"

    receipt = spannertools.get_spanners_that_dominate_component_pair(None, voice[0])

    assert len(receipt) == 0
    assert receipt == set([])


def test_spannertools_get_spanners_that_dominate_component_pair_02():
    r'''Beam and trill both dominate crack at voice[1:1].
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_component_pair(voice[0], voice[1])

    assert len(receipt) == 2
    assert (beam, 1) in receipt
    assert (trill, 2) in receipt


def test_spannertools_get_spanners_that_dominate_component_pair_03():
    r'''Glissando and trill both dominate crack at voice[2:2].
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_component_pair(voice[1], voice[2])

    assert len(receipt) == 2
    assert (glissando, 1) in receipt
    assert (trill, 4) in receipt


def test_spannertools_get_spanners_that_dominate_component_pair_04():
    r'''No spanners dominate 'crack' following voice.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_component_pair(voice[2], None)

    assert len(receipt) == 0
    assert receipt == set([])
