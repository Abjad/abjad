from abjad import *
import py.test


def test_spannertools_get_beam_spanner_attached_to_component_01():
    '''Get the only beam spanner attached to component.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)

    assert spannertools.get_beam_spanner_attached_to_component(staff[0]) is beam
    assert spannertools.get_beam_spanner_attached_to_component(staff[1]) is beam


def test_spannertools_get_beam_spanner_attached_to_component_02():
    '''Raise missing spanner error when no beam spanner attaches to component.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    assert py.test.raises(MissingSpannerError, 'spannertools.get_beam_spanner_attached_to_component(staff[0])')


def test_spannertools_get_beam_spanner_attached_to_component_03():
    '''Raise missing spanner error when no beam spanner attaches to component.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff.leaves)
    spannertools.BeamSpanner(staff.leaves)

    assert py.test.raises(ExtraSpannerError, 'spannertools.get_beam_spanner_attached_to_component(staff[0])')
