# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner_pop_01():
    r'''Remove and return rightmost component in spanner.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

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
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    result = beam.pop()

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

    assert result is voice[-1]
