# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_insert_01():
    r'''Insert component in spanner at index i.
    Add spanner to component's aggregator.
    Component then knows about spanner and vice versa.
    Not composer-safe.
    Inserting into middle of spanner may leave discontiguous spanner.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    beam._insert(1, voice[:][-1])

    assert not inspect_(voice).is_well_formed()


def test_spannertools_Spanner_insert_02():
    r'''Insert component at index zero in spanner.
    This operation does not mangle spanner.
    Operation is still not composer-safe, however.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = Beam()
    attach(beam, voice[1][:])

    assert format(voice) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
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