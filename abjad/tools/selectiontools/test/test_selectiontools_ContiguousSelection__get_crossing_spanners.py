# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_selectiontools_ContiguousSelection__get_crossing_spanners_01():
    r'''Returns unordered set of spanners crossing
    over the begin- or end-bounds of logical-voice-contiguous
    components.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    slur = spannertools.SlurSpanner()
    attach(slur, voice[1][:])
    trill = spannertools.TrillSpanner()
    attach(trill, voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 \startTrillSpan
                d'8
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

    spanners = voice.select_leaves()[:-1]._get_crossing_spanners()
    assert len(spanners) == 2
    assert slur in spanners
    assert trill in spanners


def test_selectiontools_ContiguousSelection__get_crossing_spanners_02():
    r'''Helper gets spanners that cross in from above.
    '''

    voice = Voice("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[1:2] + voice[2][0:1])

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
