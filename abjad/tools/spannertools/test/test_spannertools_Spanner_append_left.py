# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_append_left_01():
    r'''Append container to the left.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = BeamSpanner()
    attach(beam, voice[1])

    beam.append_left(voice[0])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
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

    assert inspect(voice).is_well_formed()


def test_spannertools_Spanner_append_left_02():
    r'''Spanner appends one leaf to the right.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = BeamSpanner()
    attach(beam, voice[1])

    beam.append_left(voice[0][-1])

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

    assert inspect(voice).is_well_formed()
