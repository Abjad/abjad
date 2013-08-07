# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_get_spanners_that_dominate_components_01():
    r'''Return Python list of (spanner, index) pairs.
        Each (spanner, index) pair gives a spanner which dominates
        all components in list, together with the start-index
        at which spanner attaches to subelement of first
        component in list.'''

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

    receipt = spannertools.get_spanners_that_dominate_components(voice[:1])

    "Beam and trill dominate first container."

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_02():
    r'''Beam, glissando and trill all dominante second container.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_components(voice[1:2])

    assert len(receipt) == 3
    assert (beam, 1) in receipt
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_spannertools_get_spanners_that_dominate_components_03():
    r'''Glissando and trill dominate last container.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_components(voice[-1:])

    assert len(receipt) == 2
    assert (glissando, 1) in receipt
    assert (trill, 4) in receipt


def test_spannertools_get_spanners_that_dominate_components_04():
    r'''Beam and trill dominate first two containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_components(voice[:2])

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_05():
    r'''Glissando and trill dominate last two containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_components(voice[-2:])

    assert len(receipt) == 2
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_spannertools_get_spanners_that_dominate_components_06():
    r'''Only trill dominates all three containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_components(voice[:])

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_07():
    r'''Only trill dominates voice.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_components([voice])

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_08():
    r'''Only trill dominates first two notes.
        Note that trill attaches to notes.
        Note that beam and glissando attach to containers.'''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = spannertools.get_spanners_that_dominate_components(voice.select_leaves()[:2])

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_09():
    r'''Works on empty containers.
        Implementation does not depend on component duration.'''

    t = Voice(Container([]) * 3)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.select_leaves())

    r'''
    \new Voice {
        {
        }
        {
        }
        {
        }
    }
    '''

    receipt = spannertools.get_spanners_that_dominate_components(t[:1])

    "Only beam dominates first container."

    assert len(receipt) == 1
    assert (beam, 0) in receipt
