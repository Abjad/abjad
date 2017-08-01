# -*- coding: utf-8 -*-
import abjad


def test_spannertools_DuratedComplexBeam___copy___01():

    staff = abjad.Staff([
        abjad.Container("c'32 d'32 e'32"),
        abjad.Container("f'32 g'32 a'32"),
        abjad.Container("b'32 c'32")
        ])
    durations = [abjad.inspect(x).get_duration() for x in staff]

    beam = abjad.DuratedComplexBeam(
        durations=durations,
        span_beam_count=2,
        direction=Down,
        )
    leaves = abjad.select(staff).by_leaf()
    abjad.attach(beam, leaves)

    new_staff = abjad.mutate(staff).copy()
    new_leaves = abjad.select(new_staff).by_leaf()
    new_beam = abjad.inspect(new_leaves[0]).get_spanner(abjad.Beam)

    assert format(staff) == format(new_staff)
    assert new_beam.durations == beam.durations
    assert new_beam.span_beam_count == beam.span_beam_count
    assert new_beam.isolated_nib_direction == beam.isolated_nib_direction
    assert new_beam.direction == beam.direction
