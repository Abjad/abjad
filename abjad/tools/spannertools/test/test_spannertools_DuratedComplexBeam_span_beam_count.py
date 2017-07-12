# -*- coding: utf-8 -*-
import abjad


def test_spannertools_DuratedComplexBeam_span_beam_count_01():
    r'''1-beam span between adjacent groups of 1/16th notes.
    '''

    container = abjad.Container("c'16 d'16 e'16 f'16")
    beam = abjad.DuratedComplexBeam(
        durations=[(1, 8), (1, 8)],
        span_beam_count=1,
        )
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
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

    assert abjad.inspect(container).is_well_formed()


def test_spannertools_DuratedComplexBeam_span_beam_count_02():
    r'''2-beam span between adjacent groups of 1/16th notes.
    '''

    container = abjad.Container("c'16 d'16 e'16 f'16")
    beam = abjad.DuratedComplexBeam(
        durations=[(1, 8), (1, 8)],
        span_beam_count=2,
        )
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
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

    assert abjad.inspect(container).is_well_formed()
