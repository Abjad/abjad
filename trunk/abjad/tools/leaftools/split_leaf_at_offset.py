from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import pitchtools


# TODO: This be replaced in favor of leaftools.split_leaf_at_offsets().
#       The precondition is that leaftools.split_leaf_at_offsets() must be extended to handle graces.
#       Also important to migrate over the (large-ish) set of tests for this function.
def split_leaf_at_offset(leaf, offset, fracture_spanners=False, tie_split_notes=True, tie_split_rests=False):
    r'''Split `leaf` at `offset`.

    Example 1. Split note at assignable offset. Two notes result. Do not tie notes::

        >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
        >>> beamtools.apply_beam_spanners_to_measures_in_expr(staff)
        [BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|)]
        >>> contexttools.DynamicMark('f')(staff.leaves[0])
        DynamicMark('f')(c'8)
        >>> marktools.Articulation('accent')(staff.leaves[0])
        Articulation('accent')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 -\accent \f [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> leaftools.split_leaf_at_offset(staff.leaves[0], (1, 32), tie_split_notes=False)
        ([Note("c'32")], [Note("c'16.")])

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'32 -\accent \f [ (
                c'16.
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    Example 2. Handle grace and after grace containers correctly.

        >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
        >>> beamtools.apply_beam_spanners_to_measures_in_expr(staff)
        [BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|)]
        >>> gracetools.GraceContainer("cs'16")(staff.leaves[0])
        Note("c'8")
        >>> gracetools.GraceContainer("ds'16", kind='after')(staff.leaves[0])
        Note("c'8")

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                \grace {
                    cs'16
                }
                \afterGrace
                c'8 [ (
                {
                    ds'16
                }
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> leaftools.split_leaf_at_offset(staff.leaves[0], (1, 32), tie_split_notes=False)
        ([Note("c'32")], [Note("c'16.")])

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                \grace {
                    cs'16
                }
                c'32 [ (
                \afterGrace
                c'16.
                {
                    ds'16
                }
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    Return pair.
    '''
    from abjad.tools import contexttools
    from abjad.tools import gracetools
    from abjad.tools import leaftools
    from abjad.tools import marktools
    from abjad.tools import spannertools
    from abjad.tools import tietools

    # check input
    assert isinstance(leaf, leaftools.Leaf)
    offset = durationtools.Offset(offset)

    # calculate durations
    leaf_multiplied_duration = leaf.multiplied_duration
    preprolated_duration = offset / leaf.prolation

    # handle boundary cases
    if preprolated_duration <= 0:
        return ([], [leaf])
    if leaf_multiplied_duration <= preprolated_duration:
        return ([leaf], [])

    # create new leaf
    new_leaf = componenttools.copy_components_and_remove_spanners([leaf])[0]
    componenttools.extend_in_parent_of_component(leaf, [new_leaf], grow_spanners=True)

    # adjust leaf
    gracetools.detach_grace_containers_attached_to_leaf(leaf, kind='after')

    # adjust new leaf
    gracetools.detach_grace_containers_attached_to_leaf(new_leaf, kind='grace')
    marktools.detach_marks_attached_to_component(new_leaf) 
    contexttools.detach_context_marks_attached_to_component(new_leaf)

    left_leaf_list = leaftools.set_preprolated_leaf_duration(leaf, preprolated_duration)
    right_preprolated_duration = leaf_multiplied_duration - preprolated_duration
    right_leaf_list = leaftools.set_preprolated_leaf_duration(new_leaf, right_preprolated_duration)

    leaf_left_of_split = left_leaf_list[-1]
    leaf_right_of_split = right_leaf_list[0]

    if fracture_spanners:
        spannertools.fracture_spanners_attached_to_component(leaf_left_of_split, direction=Right)

    # tie split notes, rests and chords as specified
    if  (pitchtools.is_pitch_carrier(leaf) and tie_split_notes) or \
        (not pitchtools.is_pitch_carrier(leaf) and tie_split_rests):
        tietools.apply_tie_spanner_to_leaf_pair(leaf_left_of_split, leaf_right_of_split)

    return left_leaf_list, right_leaf_list

    # TODO: make this substitution work
#    return leaftools.split_leaf_at_offsets(leaf, [offset], cyclic=False, 
#        fracture_spanners=fracture_spanners, tie_split_notes=tie_split_notes,
#        tie_split_rests=tie_split_rests)
