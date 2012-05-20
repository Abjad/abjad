from abjad import *


def test_beamtools_is_component_with_beam_spanner_attached_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = beamtools.BeamSpanner(staff.leaves)

    assert beamtools.is_component_with_beam_spanner_attached(staff[0])


def test_beamtools_is_component_with_beam_spanner_attached_02():

    assert not beamtools.is_component_with_beam_spanner_attached(Note("c'8"))
    assert not beamtools.is_component_with_beam_spanner_attached('foo')
