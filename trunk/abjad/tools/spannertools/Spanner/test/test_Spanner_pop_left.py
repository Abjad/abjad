# -*- encoding: utf-8 -*-
from abjad import *


def test_Spanner_pop_left_01():
    r'''Remove and return leftmost component in spanner.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

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

    result = p.pop_left()

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8 [
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )
    assert result is t[0]
