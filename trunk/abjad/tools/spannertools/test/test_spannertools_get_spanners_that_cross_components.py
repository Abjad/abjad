# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_get_spanners_that_cross_components_01():
    r'''Return unordered set of spanners crossing
    over the begin- or end-bounds of logical-voice-contiguous 
    components.
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

    spanners = spannertools.get_spanners_that_cross_components([voice])
    assert spanners == set([])

    spanners = spannertools.get_spanners_that_cross_components(voice.select_leaves())
    assert spanners == set([])

    spanners = spannertools.get_spanners_that_cross_components(voice[0:1])
    assert len(spanners) == 1
    assert trill in spanners

    spanners = spannertools.get_spanners_that_cross_components(voice.select_leaves()[0:1])
    assert len(spanners) == 2
    assert beam in spanners
    assert trill in spanners


def test_spannertools_get_spanners_that_cross_components_02():
    r'''Helper gets spanners that cross in from above.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[1:2] + voice[2][0:1])

    r'''
    \new Voice {
            \time 2/8
            c'8
            d'8
            \time 2/8
            e'8 [
            f'8
            \time 2/8
            g'8 ]
            a'8
    }
    '''

    spanners = spannertools.get_spanners_that_cross_components(voice.select_leaves())

    assert len(spanners) == 1
    assert beam in spanners
