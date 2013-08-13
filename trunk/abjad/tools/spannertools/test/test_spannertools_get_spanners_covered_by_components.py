# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_get_spanners_covered_by_components_01():
    r'''Return unordered set of spanners completely covered
        by the time bounds of logical-voice-contiguous components.'''

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

    spanners = spannertools.get_spanners_covered_by_components([voice])
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners

    spanners = spannertools.get_spanners_covered_by_components(voice.select_leaves())
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners

    spanners = spannertools.get_spanners_covered_by_components(voice[0:1])
    assert len(spanners) == 1
    assert beam in spanners

    spanners = spannertools.get_spanners_covered_by_components(voice.select_leaves()[0:1])
    assert spanners == set([])
