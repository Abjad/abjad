# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeam_direction_01():

    container = Container("c'16 d'16 e'16 f'16")

    beam = spannertools.DuratedComplexBeam(
        durations=[(1, 8), (1, 8)], 
        span_beam_count=1, 
        direction=Up,
        )

    attach(beam, container)

    assert systemtools.TestManager.compare(
        container,
        r'''
        {
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

    assert inspect(container).is_well_formed()
