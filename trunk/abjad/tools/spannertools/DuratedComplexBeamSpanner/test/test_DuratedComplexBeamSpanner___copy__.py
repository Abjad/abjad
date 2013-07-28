from abjad import *


def test_DuratedComplexBeamSpanner___copy___01():

    staff = Staff([
        Container("c'32 d'32 e'32"),
        Container("f'32 g'32 a'32"),
        Container("b'32 c'32")
        ])
    durations = [x._preprolated_duration for x in staff]
    beam = spannertools.DuratedComplexBeamSpanner(
        staff[:], durations=durations, span=2, direction=Down)

    new_staff = componenttools.copy_components_and_covered_spanners([staff])[0]
    new_beam = new_staff[0]._get_spanner(spannertools.BeamSpanner)

    assert staff.lilypond_format == new_staff.lilypond_format
    assert new_beam.durations == beam.durations
    assert new_beam.span == beam.span
    assert new_beam.lone == beam.lone
    assert new_beam.direction == beam.direction
