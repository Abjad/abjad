# -*- encoding: utf-8 -*-
from abjad import *


def test_MeasuredComplexBeamSpanner_direction_01():

    t = Staff(Measure((2, 16), notetools.make_repeated_notes(2, Duration(1, 16))) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/16
            c'16
            d'16
        }
        {
            \time 2/16
            e'16
            f'16
        }
        {
            \time 2/16
            g'16
            a'16
        }
    }
    '''

    beam = spannertools.MeasuredComplexBeamSpanner(t[:], direction=Down)

    r'''
    \new Staff {
        {
            \time 2/16
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 _ [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #1
            d'16
        }
        {
            \time 2/16
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #2
            e'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #1
            f'16
        }
        {
            \time 2/16
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #2
            g'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            a'16 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            {
                \time 2/16
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 _ [
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                d'16
            }
            {
                \time 2/16
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                e'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #1
                f'16
            }
            {
                \time 2/16
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #2
                g'16
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                a'16 ]
            }
        }
        '''
        )
