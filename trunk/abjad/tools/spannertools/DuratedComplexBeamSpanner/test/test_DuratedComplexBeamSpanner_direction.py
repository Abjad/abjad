# -*- encoding: utf-8 -*-
from abjad import *


def test_DuratedComplexBeamSpanner_direction_01():
    voice = Voice("c'16 d'16 e'16 f'16")
    spannertools.DuratedComplexBeamSpanner(voice, durations=[(1, 8), (1, 8)], span=1, direction=Up)

    r'''
    \new Voice {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 ^ [
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #1
        d'16
        \set stemLeftBeamCount = #1
        \set stemRightBeamCount = #2
        e'16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #0
        f'16 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 ^ [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #1
            d'16
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #2
            e'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 ]
        }
        '''
        )
