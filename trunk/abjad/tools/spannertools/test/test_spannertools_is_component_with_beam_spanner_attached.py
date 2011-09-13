from abjad import *


def test_spannertools_is_component_with_beam_spanner_attached_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)

    assert spannertools.is_component_with_beam_spanner_attached(staff[0])


def test_spannertools_is_component_with_beam_spanner_attached_02():

    assert not spannertools.is_component_with_beam_spanner_attached(Note("c'8"))
    assert not spannertools.is_component_with_beam_spanner_attached('foo')
