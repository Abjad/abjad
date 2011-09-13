from abjad import *

def test_spannertools_get_spanners_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)
    first_slur = spannertools.SlurSpanner(staff.leaves[:2])
    second_slur = spannertools.SlurSpanner(staff.leaves[2:])
    crescendo = spannertools.CrescendoSpanner(staff.leaves)

    r'''
    \new Staff {
        c'8 [ \< (
        d'8 )
        e'8 (
        f'8 ] \! )
    }
    '''

    leaf = staff[0]

    spanners = spannertools.get_spanners_attached_to_component(leaf)
    assert spanners == set([beam, first_slur, crescendo])

    spanners = spannertools.get_spanners_attached_to_component(leaf, spannertools.BeamSpanner)
    assert spanners == set([beam])

    spanner_klasses = (spannertools.BeamSpanner, spannertools.SlurSpanner)
    spanners = spannertools.get_spanners_attached_to_component(leaf, spanner_klasses)
    assert spanners == set([beam, first_slur])

    spanners = spannertools.get_spanners_attached_to_component(leaf, tietools.TieSpanner)
    assert spanners == set([])
