# -*- encoding: utf-8 -*-
from abjad import *


def test_DuratedComplexBeamSpanner_span_01():
    r'''1-beam span between adjacent groups of 1/16th notes.
    '''

    voice = Voice("c'16 d'16 e'16 f'16")
    spannertools.DuratedComplexBeamSpanner(voice, durations=[(1, 8), (1, 8)], span=1)

    r'''
    \new Voice {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 [
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
        voice.lilypond_format,
        r'''
        \new Voice {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
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



def test_DuratedComplexBeamSpanner_span_02():
    r'''2-beam span between adjacent groups of 1/16th notes.
    '''

    t = Voice("c'16 d'16 e'16 f'16")
    spannertools.DuratedComplexBeamSpanner(t, durations=[(1, 8), (1, 8)], span=2)

    r'''
    \new Voice {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 [
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #2
        d'16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #2
        e'16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #0
        f'16 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            d'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 ]
        }
        '''
        )
