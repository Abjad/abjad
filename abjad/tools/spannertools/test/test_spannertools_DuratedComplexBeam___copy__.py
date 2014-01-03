# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeam___copy___01():

    staff = Staff([
        Container("c'32 d'32 e'32"),
        Container("f'32 g'32 a'32"),
        Container("b'32 c'32")
        ])
    durations = [inspect(x).get_duration() for x in staff]

    beam = spannertools.DuratedComplexBeam(
        durations=durations, 
        span_beam_count=2, 
        direction=Down,
        )
    attach(beam, staff[:])

    new_staff = mutate(staff).copy()
    new_beam = inspect(new_staff[0]).get_spanner(Beam)

    assert format(staff) == format(new_staff)
    assert new_beam.durations == beam.durations
    assert new_beam.span_beam_count == beam.span_beam_count
    assert new_beam.isolated_nib_direction == beam.isolated_nib_direction
    assert new_beam.direction == beam.direction
