from abjad import *


def test_spannertools_get_spanners_attached_to_any_improper_parent_of_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)
    slur = spannertools.SlurSpanner(staff.leaves)
    trill = spannertools.TrillSpanner(staff)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8
        e'8
        f'8 ] ) \stopTrillSpan
    }
    '''

    assert spannertools.get_spanners_attached_to_any_improper_parent_of_component(staff[0]) == \
        set([beam, slur, trill])
    assert spannertools.get_spanners_attached_to_any_improper_parent_of_component(staff) == \
        set([trill])
