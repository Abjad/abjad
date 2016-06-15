# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeam_span_beam_count_01():
    r'''1-beam span between adjacent groups of 1/16th notes.
    '''

    container = Container("c'16 d'16 e'16 f'16")
    beam = spannertools.DuratedComplexBeam(
        durations=[(1, 8), (1, 8)],
        span_beam_count=1,
        )
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
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

    assert inspect_(container).is_well_formed()


def test_spannertools_DuratedComplexBeam_span_beam_count_02():
    r'''2-beam span between adjacent groups of 1/16th notes.
    '''

    container = Container("c'16 d'16 e'16 f'16")
    beam = spannertools.DuratedComplexBeam(
        durations=[(1, 8), (1, 8)],
        span_beam_count=2,
        )
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
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

    assert inspect_(container).is_well_formed()