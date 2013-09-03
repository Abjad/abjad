# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_ContiguousSelection__get_dominant_spanners_01():
    r'''Return Python list of (spanner, index) pairs.
    Each (spanner, index) pair gives a spanner which dominates
    all components in list, together with the start-index
    at which spanner attaches to subelement of first
    component in list.
    Beam and trill dominate first container.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    assert testtools.compare(
        voice,
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


def test_ContiguousSelection__get_dominant_spanners_02():
    r'''Beam, glissando and trill all dominante second container.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = voice[1:2]._get_dominant_spanners()

    assert len(receipt) == 3
    assert (beam, 1) in receipt
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_ContiguousSelection__get_dominant_spanners_03():
    r'''Glissando and trill dominate last container.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = voice[-1:]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (glissando, 1) in receipt
    assert (trill, 4) in receipt


def test_ContiguousSelection__get_dominant_spanners_04():
    r'''Beam and trill dominate first two containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt= voice[:2]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_ContiguousSelection__get_dominant_spanners_05():
    r'''Glissando and trill dominate last two containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = voice[-2:]._get_dominant_spanners()

    assert len(receipt) == 2
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_ContiguousSelection__get_dominant_spanners_06():
    r'''Only trill dominates all three containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = voice[:]._get_dominant_spanners()

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_ContiguousSelection__get_dominant_spanners_07():
    r'''Only trill dominates voice.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = select(voice)._get_dominant_spanners()

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_ContiguousSelection__get_dominant_spanners_08():
    r'''Only trill dominates first two notes.
    Note that trill attaches to notes.
    Note that beam and glissando attach to containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    receipt = voice.select_leaves()[:2]._get_dominant_spanners()

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_ContiguousSelection__get_dominant_spanners_09():
    r'''Works on empty containers.
    Implementation does not depend on component duration.
    Only beam dominates first container.
    '''

    voice = Voice(Container([]) * 3)
    beam = spannertools.BeamSpanner(voice[:2])
    glissando = spannertools.GlissandoSpanner(voice[1:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    assert testtools.compare(
        voice,
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
        )

    receipt = voice[:1]._get_dominant_spanners()

    assert len(receipt) == 1
    assert (beam, 0) in receipt
