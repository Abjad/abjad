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

    spanner_classes = (spannertools.SlurSpanner, )
    spanners = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        staff, spanner_classes=spanner_classes)
    assert spanners == set([first_slur, second_slur])

    spanner_classes = (spannertools.BeamSpanner, spannertools.SlurSpanner)
    spanners = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        staff, spanner_classes=spanner_classes)
    assert spanners == set([beam, first_slur, second_slur])

    spanner_classes = (spannertools.TrillSpanner, )
    spanners = spannertools.get_spanners_attached_to_any_proper_child_of_component(
        staff, spanner_classes=spanner_classes)
    assert spanners == set([])
