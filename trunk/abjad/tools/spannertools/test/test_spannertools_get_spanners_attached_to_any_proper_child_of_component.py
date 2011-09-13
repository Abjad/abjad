from abjad import *


def test_spannertools_get_spanners_attached_to_any_proper_child_of_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)
    first_slur = spannertools.SlurSpanner(staff.leaves[:2])
    second_slur = spannertools.SlurSpanner(staff.leaves[2:])
    trill = spannertools.TrillSpanner(staff)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8 )
        e'8 (
        f'8 ] ) \stopTrillSpan
    }
    '''

    spanners = spannertools.get_spanners_attached_to_any_proper_child_of_component(staff)
    assert spanners == set([beam, first_slur, second_slur])
    assert trill not in spanners

    spanners = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        staff, spannertools.SlurSpanner)
    assert spanners == set([first_slur, second_slur])

    spanners = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        staff, (spannertools.BeamSpanner, spannertools.SlurSpanner))
    assert spanners == set([beam, first_slur, second_slur])

    spanners = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        staff, spannertools.TrillSpanner)
    assert spanners == set([])
