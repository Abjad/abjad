# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_SliceSelection__withdraw_from_crossing_spanners_01():
    r'''Withdraw thread-contiguous components from crossing spanners.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[0][:])
    slur = spannertools.SlurSpanner(voice[1][:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    r'''
    \new Voice {
        {
            c'8 [ \startTrillSpan
            d'8 ]
        }
        {
            e'8 (
            f'8 ) \stopTrillSpan
        }
    }
    '''

    spanners = spannertools.get_spanners_contained_by_components([voice])
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners

    voice_selection = selectiontools.SliceSelection([voice])
    voice_selection._withdraw_from_crossing_spanners()
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners


def test_SliceSelection__withdraw_from_crossing_spanners_02():
    r'''Withdraw thread-contiguous components from crossing spanners.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[0][:])
    slur = spannertools.SlurSpanner(voice[1][:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    r'''
    \new Voice {
        {
            c'8 [ \startTrillSpan
            d'8 ]
        }
        {
            e'8 (
            f'8 ) \stopTrillSpan
        }
    }
    '''

    spanners = spannertools.get_spanners_contained_by_components(voice[0:1])
    assert len(spanners) == 2
    assert beam in spanners
    assert trill in spanners

    voice[:1]._withdraw_from_crossing_spanners()

    r'''
    \new Voice {
        {
            c'8 [
            d'8 ]
        }
        {
            e'8 ( \startTrillSpan
            f'8 ) \stopTrillSpan
        }
    }
    '''

    spanners = spannertools.get_spanners_contained_by_components(voice[0:1])
    assert len(spanners) == 1
    assert beam in spanners

    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            {
                c'8 [
                d'8 ]
            }
            {
                e'8 ( \startTrillSpan
                f'8 ) \stopTrillSpan
            }
        }
        '''
        )


def test_SliceSelection__withdraw_from_crossing_spanners_03():
    r'''Withdraw thread-contiguous components from crossing spanners.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beam = spannertools.BeamSpanner(t[0][:])
    slur = spannertools.SlurSpanner(t[1][:])
    trill = spannertools.TrillSpanner(t.select_leaves())

    r'''
    \new Voice {
        {
            c'8 [ \startTrillSpan
            d'8 ]
        }
        {
            e'8 (
            f'8 ) \stopTrillSpan
        }
    }
    '''

    spanners = spannertools.get_spanners_contained_by_components(t.select_leaves()[2:3])
    assert len(spanners) == 2
    assert slur in spanners
    assert trill in spanners

    t.select_leaves()[2:3]._withdraw_from_crossing_spanners()

    spanners = spannertools.get_spanners_contained_by_components(t.select_leaves()[2:3])
    assert spanners == set([])

    "Operation leaves score tree in weird state."
    "Both slur and trill are now discontiguous."

    assert not select(t).is_well_formed()
