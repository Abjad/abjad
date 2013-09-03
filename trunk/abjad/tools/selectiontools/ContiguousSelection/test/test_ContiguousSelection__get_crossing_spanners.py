# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_ContiguousSelection__get_crossing_spanners_01():
    r'''Return unordered set of spanners crossing
    over the begin- or end-bounds of logical-voice-contiguous 
    components.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[0][:])
    slur = spannertools.SlurSpanner(voice[1][:])
    trill = spannertools.TrillSpanner(voice.select_leaves())

    assert testtools.compare(
        voice,
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
        )

    spanners = select(voice)._get_crossing_spanners()
    assert spanners == set([])

    spanners = voice.select_leaves()._get_crossing_spanners()
    assert spanners == set([])

    spanners = voice[:1]._get_crossing_spanners()
    assert len(spanners) == 1
    assert trill in spanners

    spanners = voice.select_leaves()[:1]._get_crossing_spanners()
    assert len(spanners) == 2
    assert beam in spanners
    assert trill in spanners


def test_ContiguousSelection__get_crossing_spanners_02():
    r'''Helper gets spanners that cross in from above.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[1:2] + voice[2][0:1])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8 [
                f'8
            }
            {
                g'8 ]
                a'8
            }
        }
        '''
        )

    spanners = voice.select_leaves()._get_crossing_spanners()

    assert len(spanners) == 1
    assert beam in spanners
