from abjad import *


def test_BeamSpanner_fuse_01():
    '''Fuse by reference to the right.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    left = spannertools.BeamSpanner(staff[:2])
    right = spannertools.BeamSpanner(staff[2:4])

    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))
    assert left[:] == staff[:2]
    assert left.components == tuple(staff[:2])
    assert right[:] == staff[2:4]
    assert right.components == tuple(staff[2:4])

    left.fuse(right)
    spanners = \
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)

    assert len(spanners) == 1
