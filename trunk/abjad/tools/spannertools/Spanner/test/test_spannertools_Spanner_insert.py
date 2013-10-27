# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_insert_01():
    r'''Insert component in spanner at index i.
    Add spanner to component's aggregator.
    Component then knows about spanner and vice versa.
    Not composer-safe.
    Inserting into middle of spanner may leave discontiguous spanner.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    beam._insert(1, voice.select_leaves()[-1])

    # Interior insert leaves discontiguous spanner: 
    # spannertools.BeamSpanner(c'8, f'8, d'8)

    assert not inspect(voice).is_well_formed()


def test_spannertools_Spanner_insert_02():
    r'''Insert component at index zero in spanner.
    This operation does not mangle spanner.
    Operation is still not composer-safe, however.
    Note that beam.append() and beam.append_left() are composer-safe.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[1])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    beam._insert(0, voice[0][1])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8 [
            }
            {
                e'8
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )
