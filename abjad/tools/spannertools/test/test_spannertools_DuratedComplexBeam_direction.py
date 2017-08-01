# -*- coding: utf-8 -*-
import abjad


def test_spannertools_DuratedComplexBeam_direction_01():

    container = abjad.Container("c'16 d'16 e'16 f'16")

    beam = abjad.DuratedComplexBeam(
        durations=[(1, 8), (1, 8)],
        span_beam_count=1,
        direction=Up,
        )

    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
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

    assert abjad.inspect(container).is_well_formed()
